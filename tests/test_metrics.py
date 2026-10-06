import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cli'))
from axiomcli.metrics import report

class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root/'sdd').mkdir()
        (self.root/'proof.txt').write_text('synthetic output')
        self.now = datetime(2026, 10, 6, 12, tzinfo=timezone.utc)
        self.observation = dict(at='2026-10-04T12:00:00Z',path='proof.txt',sha256=hashlib.sha256(b'synthetic output').hexdigest(),mode='simulated',passed=8,failed=0,skipped=0)
        self.task = dict(id='TASK-1',owner='private-owner',next_action='private-action',blocker=None,required_mode='real',observations=[self.observation])
    def run_report(self):
        (self.root/'sdd/progress.json').write_text(json.dumps(dict(version=1,tasks=[self.task])))
        return report(self.root,now=self.now)
    def test_missing_and_no_evidence(self):
        self.assertEqual(report(self.root)['status'],'unavailable')
        self.task['observations']=[]
        self.assertEqual(self.run_report()['tasks'][0]['state'],'no_evidence')
    def test_duplicate_proof_does_not_refresh(self):
        self.task['observations'].append(dict(self.observation,at='2026-10-06T11:00:00Z'))
        result=self.run_report()['tasks'][0]
        self.assertEqual(result['age_hours'],48)
        self.assertTrue(result['stale'])
        self.assertEqual(result['state'],'real_evidence_required')
    def test_counts_and_mode(self):
        for updates,expected in [({'skipped':8,'passed':0},'incomplete_checks'),({'failed':1},'incomplete_checks'),({'mode':'real'},'declared_checks_supported')]:
            with self.subTest(updates=updates):
                self.task['observations']=[dict(self.observation,**updates)]
                self.assertEqual(self.run_report()['tasks'][0]['state'],expected)
    def test_invalid_observations(self):
        for updates in [dict(at='2027-01-01T00:00:00Z'),dict(at='2026-10-01'),dict(passed=True),dict(sha256='0'*64),dict(path='../outside'),dict(path='/etc/passwd')]:
            with self.subTest(updates=updates):
                self.task['observations']=[dict(self.observation,**updates)]
                self.assertEqual(self.run_report()['tasks'][0]['state'],'invalid_evidence')
    def test_symlink_and_directory_denied(self):
        (self.root/'link').symlink_to(self.root/'proof.txt')
        for path in ['link','sdd']:
            self.task['observations']=[dict(self.observation,path=path)]
            self.assertEqual(self.run_report()['tasks'][0]['state'],'invalid_evidence')
    def test_report_privacy_and_read_only(self):
        self.task['blocker']='private-blocker'
        self.run_report()
        before={p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        text=json.dumps(report(self.root,now=self.now))
        for secret in ['private-owner','private-action','private-blocker','synthetic output']:
            self.assertNotIn(secret,text)
        self.assertEqual(before,{p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
    def test_invalid_document_and_options(self):
        (self.root/'sdd/progress.json').write_text('{"version":1,"version":1,"tasks":[]}')
        self.assertEqual(report(self.root)['status'],'invalid')
        for limit in [0,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError): report(self.root,stale_hours=limit)
    def test_cli(self):
        cli=Path(__file__).resolve().parents[1]/'cli/axiom.py'
        p=subprocess.run([sys.executable,str(cli),'metrics','--target',str(self.root)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0)
        self.assertEqual(json.loads(p.stdout)['status'],'unavailable')
        p=subprocess.run([sys.executable,str(cli),'metrics','--stale-hours','nan'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2)
