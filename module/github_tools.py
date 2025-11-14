import os
import re
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse


class GitHubTools:
    """GitHub工具类，提供GitHub项目信息获取功能"""
    
    @staticmethod
    def get_github_repo_info(repo_url: str) -> Optional[Dict[str, Any]]:
        """
        获取GitHub仓库的最新版本、更新日期和更新说明
        
        Args:
            repo_url: GitHub仓库URL
            
        Returns:
            包含版本信息的字典，格式如下：
            {
                "repo_name": "仓库名称",
                "latest_version": "最新版本号",
                "update_date": "更新日期",
                "release_notes": "更新说明",
                "error": "错误信息（如果有）"
            }
        """
        try:
            # 解析仓库URL
            parsed_url = urlparse(repo_url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # 支持多种GitHub URL格式
            if len(path_parts) >= 2:
                owner = path_parts[0]
                repo = path_parts[1]
            else:
                return {
                    "error": "无效的GitHub仓库URL格式"
                }
            
            # 构造API URL
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            
            # Prepare headers with authentication if available
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'MCP-GitHub-Tool'
            }
            
            # Check if there's a GitHub token in environment variables
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                headers['Authorization'] = f'token {github_token}'
            
            response = requests.get(api_url, headers=headers)
            
            if response.status_code == 200:
                release_data = response.json()
                
                # 提取所需信息
                repo_name = f"{owner}/{repo}"
                latest_version = release_data.get('tag_name', 'N/A')
                update_date = release_data.get('published_at', 'N/A')
                release_notes = release_data.get('body', 'No release notes available')
                
                # 格式化日期
                if update_date != 'N/A':
                    # 将ISO格式日期转换为更易读的格式
                    update_date = update_date.split('T')[0]  # 只取日期部分
                
                return {
                    "repo_name": repo_name,
                    "latest_version": latest_version,
                    "update_date": update_date,
                    "release_notes": release_notes
                }
            elif response.status_code == 404:
                # 可能是没有发布版本，尝试获取最新提交信息
                return GitHubTools._get_repo_commit_info(owner, repo, headers)
            elif response.status_code == 403:
                return {
                    "error": f"API访问被拒绝 (403)。这可能是由于GitHub API速率限制。请设置GITHUB_TOKEN环境变量以提高API配额。"
                }
            else:
                return {
                    "error": f"获取仓库信息失败，状态码: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "error": f"获取仓库信息时发生错误: {str(e)}"
            }
    
    @staticmethod
    def _get_repo_commit_info(owner: str, repo: str, headers: dict) -> Optional[Dict[str, Any]]:
        """
        当没有发布版本时，获取仓库的最新提交信息作为替代
        
        Args:
            owner: 仓库所有者
            repo: 仓库名
            headers: 请求头（包含认证信息）
            
        Returns:
            包含提交信息的字典
        """
        try:
            # 获取仓库信息
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            
            response = requests.get(api_url, headers=headers)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                repo_name = f"{owner}/{repo}"
                latest_version = "No releases"
                update_date = repo_data.get('updated_at', 'N/A').split('T')[0]
                release_notes = "Repository has no official releases, only commits"
                
                return {
                    "repo_name": repo_name,
                    "latest_version": latest_version,
                    "update_date": update_date,
                    "release_notes": release_notes
                }
            elif response.status_code == 403:
                return {
                    "error": f"API访问被拒绝 (403)。这可能是由于GitHub API速率限制。请设置GITHUB_TOKEN环境变量以提高API配额。"
                }
            else:
                return {
                    "error": f"获取仓库信息失败，状态码: {response.status_code}"
                }
        except Exception as e:
            return {
                "error": f"获取仓库信息时发生错误: {str(e)}"
            }