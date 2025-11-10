import os
from typing import Optional, Dict, Any
from git import Repo, Commit
from git.diff import Diff


class GitTools:
    """Git工具类，提供各种Git操作功能"""
    
    def __init__(self, repo_path: str = None):
        """
        初始化Git工具类
        
        Args:
            repo_path: Git仓库路径，如果为None则使用当前目录
        """
        self.repo_path = repo_path or os.getcwd()
        self.repo = Repo(self.repo_path)
    
    def get_diff(self, file_path: str, commit_hash: str, ignore_whitespace: bool = True) -> Dict[str, Any]:
        """
        获取指定commit中文件的改动详情
        
        Args:
            file_path: 文件路径（相对于仓库根目录）
            commit_hash: commit哈希值
            ignore_whitespace: 是否忽略空白字符变化（包括换行符）
            
        Returns:
            包含文件改动详情的字典，包含以下字段：
            - file_path: 文件路径
            - commit_hash: commit哈希
            - diff_text: diff文本内容
            - change_type: 变更类型（A:新增, M:修改, D:删除, R:重命名）
            - additions: 新增行数
            - deletions: 删除行数
            - is_binary: 是否为二进制文件
            
        Raises:
            ValueError: 当commit不存在或文件不存在时抛出异常
        """
        try:
            # 获取指定commit
            commit = self.repo.commit(commit_hash)
            
            # 获取该commit的父commit（如果有的话）
            parent_commit = commit.parents[0] if commit.parents else None
            
            # 获取文件在该commit中的diff
            if parent_commit:
                # 如果有父commit，比较当前commit和父commit，确保生成patch内容
                if ignore_whitespace:
                    diff_index = parent_commit.diff(commit, paths=[file_path], create_patch=True, ignore_blank_lines=True, ignore_space_change=True)
                else:
                    diff_index = parent_commit.diff(commit, paths=[file_path], create_patch=True)
            else:
                # 如果是初始commit，比较空树和当前commit
                if ignore_whitespace:
                    diff_index = commit.diff(None, paths=[file_path], create_patch=True, ignore_blank_lines=True, ignore_space_change=True)
                else:
                    diff_index = commit.diff(None, paths=[file_path], create_patch=True)
            
            if not diff_index:
                raise ValueError(f"文件 {file_path} 在commit {commit_hash} 中没有改动")
            
            # 获取第一个diff对象（因为paths参数指定了具体文件）
            diff_obj = diff_index[0]
            
            # 解析diff信息
            result = {
                'file_path': file_path,
                'commit_hash': commit_hash,
                'diff_text': diff_obj.diff.decode('utf-8') if diff_obj.diff else '',
                'change_type': self._get_change_type(diff_obj),
                'additions': self._count_additions(diff_obj),
                'deletions': self._count_deletions(diff_obj),
                'is_binary': diff_obj.a_blob and diff_obj.a_blob.data_stream is None
            }
            
            return result
            
        except Exception as e:
            raise ValueError(f"获取diff失败: {str(e)}")
    
    def _get_change_type(self, diff_obj: Diff) -> str:
        """获取变更类型"""
        if diff_obj.new_file:
            return 'A'  # 新增
        elif diff_obj.deleted_file:
            return 'D'  # 删除
        elif diff_obj.renamed_file:
            return 'R'  # 重命名
        else:
            return 'M'  # 修改
    
    def _count_additions(self, diff_obj: Diff) -> int:
        """统计新增行数"""
        if not diff_obj.diff:
            return 0
        
        diff_text = diff_obj.diff.decode('utf-8')
        # 统计以'+'开头的行（排除diff头信息）
        additions = [line for line in diff_text.split('\n') 
                    if line.startswith('+') and not line.startswith('+++')]
        
        # 过滤掉只是换行符变化的行
        real_additions = []
        for i, line in enumerate(additions):
            # 检查对应的删除行是否存在，如果只是换行符变化，则不计入
            deletion_line = line[1:]  # 去掉开头的'+'
            has_corresponding_deletion = False
            
            # 在删除行中查找对应的行
            deletions = [d_line for d_line in diff_text.split('\n') 
                        if d_line.startswith('-') and not d_line.startswith('---')]
            
            for del_line in deletions:
                if del_line[1:].strip() == deletion_line.strip():
                    has_corresponding_deletion = True
                    break
            
            # 如果没有对应的删除行，或者内容有实质性变化，才计入
            if not has_corresponding_deletion or line.strip() != deletion_line.strip():
                real_additions.append(line)
        
        return len(real_additions)
    
    def _count_deletions(self, diff_obj: Diff) -> int:
        """统计删除行数"""
        if not diff_obj.diff:
            return 0
        
        diff_text = diff_obj.diff.decode('utf-8')
        # 统计以'-'开头的行（排除diff头信息）
        deletions = [line for line in diff_text.split('\n') 
                    if line.startswith('-') and not line.startswith('---')]
        
        # 过滤掉只是换行符变化的行
        real_deletions = []
        for i, line in enumerate(deletions):
            # 检查对应的新增行是否存在，如果只是换行符变化，则不计入
            addition_line = line[1:]  # 去掉开头的'-'
            has_corresponding_addition = False
            
            # 在新增行中查找对应的行
            additions = [a_line for a_line in diff_text.split('\n') 
                        if a_line.startswith('+') and not a_line.startswith('+++')]
            
            for add_line in additions:
                if add_line[1:].strip() == addition_line.strip():
                    has_corresponding_addition = True
                    break
            
            # 如果没有对应的新增行，或者内容有实质性变化，才计入
            if not has_corresponding_addition or line.strip() != addition_line.strip():
                real_deletions.append(line)
        
        return len(real_deletions)


def get_diff(file_path: str, commit_hash: str, repo_path: str = None) -> Dict[str, Any]:
    """
    便捷函数：获取指定commit中文件的改动详情
    
    Args:
        file_path: 文件路径（相对于仓库根目录）
        commit_hash: commit哈希值
        repo_path: Git仓库路径，如果为None则使用当前目录
        
    Returns:
        包含文件改动详情的字典
    """
    git_tools = GitTools(repo_path)
    return git_tools.get_diff(file_path, commit_hash)


if __name__ == "__main__":
    # 示例用法
    git_tools = GitTools('/Volumes/M0/View/dev')

    
    # 示例：获取最近一次commit中某个文件的diff
    try:
        # 获取最新的commit
        latest_commit = git_tools.repo.head.commit.hexsha
        print(f"latest_commit: {latest_commit}")
        # 获取某个文件的diff（这里用README.md作为示例）
        if os.path.exists('README.md'):
            diff_info = git_tools.get_diff('/Volumes/M0/View/dev/web/VFM_webservice/SyncModule/SyncModule.php', latest_commit)
            print(f"diff_info: {diff_info}")
            print(f"文件: {diff_info['file_path']}")
            print(f"Commit: {diff_info['commit_hash']}")
            print(f"变更类型: {diff_info['change_type']}")
            print(f"新增行数: {diff_info['additions']}")
            print(f"删除行数: {diff_info['deletions']}")
            print(f"是否为二进制文件: {diff_info['is_binary']}")
            print("Diff内容:")
            print(diff_info['diff_text'])
        else:
            print("README.md文件不存在，无法演示")
            
    except Exception as e:
        print(f"示例执行失败: {e}")