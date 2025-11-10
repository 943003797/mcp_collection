from mcp.server.fastmcp import FastMCP
from module.file_system import FileSystem
from module.cosyvoice_v1 import Cosyvoice
# from module.auto_cut import autoCut
from module.git_tools import GitTools

mcp = FastMCP("mcp_collection", port=8000)

@mcp.tool()
def get_git_diff(repository_path: str, file_path: str, commit_hash: str) -> str:
    """
    使用这个工具获取指定文件在指定commit中的diff内容
    参数:
        repository_path: git仓库路径
        file_path: 文件路径
        commit_hash: commit哈希值
    """
    git = GitTools(repository_path);
    diff_result = git.get_diff(file_path, commit_hash)
    # 如果返回的是字典，则转换为字符串
    if isinstance(diff_result, dict):
        return str(diff_result)
    return diff_result
def get_last_email(imap_server: str, port: int, email_address: str, password: str, inbox: str, subject: str) -> str:
    """
    使用这个工具获取指定邮箱中最新的邮件内容
    参数:
        imap_server: IMAP服务器地址
        port: IMAP服务器端口
        email_address: 邮箱地址
        password: 邮箱密码
        inbox: 收件箱名称
        subject: 邮件主题(可选,为空则获取最新邮件)
    返回:
        str: 邮件内容
        如果没有找到匹配的邮件则返回空字符串
    """
    result = EmailTools.getLastEmail(imap_server, port, email_address, password, inbox, subject)
    if result is None:
        return ""  # 如果返回None则返回空字符串
    return result

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    使用这个工具读取文件内容
    参数:
        file_path: 文件路径
    """
    return FileSystem.read_file(file_path)

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Use this tool to write content to a specified file
    Parameters:
        file_path: Target file path
        content: Content to write
        
    Returns:
        str: Operation result string
        May raise:
            FileNotFoundError: When file path does not exist
            IOError: When write operation fails
    """
    return FileSystem.write_file(file_path, content)

@mcp.tool()
def copy_dir(from_path: str, to_path: str) -> str:
    """
    This tool is used to copy files from one directory to another. A new directory named with current timestamp will be created in the destination path, and all files (excluding subdirectories) from source directory will be copied to it.
    Parameters:
        from_path: Source directory path containing files to copy
        to_path: Destination directory path where files will be copied to
    Returns:
        success: When files are copied successfully
        FileNotFoundError: When source directory does not exist
    """
    return FileSystem.copy_dir(from_path, to_path)

@mcp.tool()
def create_text_to_audio(text: str, out_path: str) -> str:
    """
    This tool is used to convert text into audio. Input the text and the output directory, and the audio will be generated and saved to the specified directory.
    Parameters:
        text: String text
        out_path: Output directory for the audio
    Returns:
        Success: Operation success
        Failed: Operation failed
    """
    return Cosyvoice.generate_audio(text, out_path)

@mcp.tool()
def auto_cut(draft_path: str) -> str:
    """
    This tool can achieve automatic video editing by specifying the draft path
    Parameters:
        draft_path: Draft path
    Returns:
        success: When files are copied successfully
    """
    ac = autoCut(draft_path, '浮光.mp3','水墨山河.mp4');
    ac.general_draft();
    return "Success"

if __name__ == "__main__":
    mcp.run(transport='sse')