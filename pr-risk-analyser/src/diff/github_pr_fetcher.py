import requests

class GitHubPRFetcher:
    
    def __init__ (self,token):
        self.token=token
        
    def get_pr_files(self,owner,repo,pr_number):
        
        url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
        
        headers={
            "Authorization": f"token {self.token}"}
        
        response=requests.get(url,headers=headers)
        
        return response.json()
    
    def get_diff_text(self,files):
        all_patches=[]
        
        for changed_file in files:
            if "patch" in changed_file:
                results=changed_file["patch"]
                all_patches.append(results)
        return "\n".join(all_patches)