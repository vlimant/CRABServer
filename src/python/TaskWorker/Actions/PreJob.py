
import os
import htcondor

from ApmonIf import ApmonIf

class PreJob:

    def update_dashboard(self, retry, id, reqname, backend):

        if not self.task_ad:
            continue

        params = {'tool': 'crab3',
                  'SubmissionType':'direct',
                  'JSToolVersion': '3.3.0',
                  'tool_ui': os.environ.get('HOSTNAME',''),
                  'scheduler': 'GLIDEIN',
                  'GridName': self.task_ad['CRAB_UserDN'],
                  'ApplicationVersion': self.task_ad['CRAB_JobSW'],
                  'taskType': 'analysis',
                  'vo': 'cms',
                  'CMSUser': self.task_ad['CRAB_UserHN'],
                  'user': self.task_ad['CRAB_UserHN'],
                  'taskId': self.task_ad['CRAB_ReqName'],
                  'datasetFull': self.task_ad['CRAB_InputData'],
                  'resubmitter': self.task_ad['CRAB_UserHN'],
                  'exe': 'cmsRun',
                  'jobId': ("%d_https://glidein.cern.ch/%d/%s_%d" % (id, id, self.task_ad['CRAB_ReqName']), retry),
                  'sid': "https://glidein.cern.ch/%d/%s" % (id, self.task_ad['CRAB_ReqName']),
                  'broker': backend,
                  'bossId': str(id),
                  'localId' : '',
                 }

        apmon = ApmonIf()
        self.logger.debug("Dashboard task info: %s" % str(params))
        apmon.sendToML(params)
        apmon.free()


    def get_task_ad(self, reqname):
        try:
            schedd = htcondor.Schedd()
            results = schedd.query('CRAB_ReqName =?= "%s" && TaskType =?= "ROOT"' % reqname)
        except Exception:
            print traceback.format_exc()
            return
        if results:
            self.task_ad = results[0]


    def alter_submit(self, retry, id):
        new_submit_text = '+CRAB_Retry = %d\n' % retry
        with open("Job.%d.submit" % id, "r") as fd:
            new_submit_text += fd.read()
        with open("Job.%d.submit" % id, "w") as fd:
            fd.write(new_submit_text)


    def execute(self, *args):
        retry_num = int(args[0])
        crab_id = int(args[1])
        reqname = args[2]
        backend = args[3]
        self.alter_submit(retry_num, crab_id)
        if retry_num != 0:
            self.update_dashboard(retry, id, reqname, backend)
        os.execv("/bin/sleep", ["sleep", str(int(args[0])*60)])

