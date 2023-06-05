class BFEntity():
    def __init__(self):
        # event information
        self.event_type=None
        self.commit_url=None

        # bug-fix pair information
        self.buggy_file_code=None
        self.fix_file_code=None
        self.commit_message=None
        self.patch=None
        self.fault_type=None
        self.fault_location=None

        # extra information for PullRequest Event
        self.issue_url=None
        self.title_url=None
        self.patch_url=None

    def init_repo_info(self,repo_url,repo_stars,repo_language):
        self.repo_url = repo_url
        self.repo_stars = repo_stars
        self.repo_language = repo_language

