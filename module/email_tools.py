import imaplib
import email
from email.header import decode_header
import ssl
from typing import Optional


class EmailTools:
    """邮件处理类，提供邮件读取功能"""
    
    @staticmethod
    def getLastEmail(imap_server: str, port: int, email_address: str, password: str, inbox: str, subject: str) -> Optional[str]:
        """
        获取指定主题的最后一封邮件内容
        
        Args:
            imap_server: IMAP服务器地址
            port: IMAP端口（通常为993或143）
            email_address: 邮箱地址
            password: 邮箱密码
            subject: 要搜索的邮件主题
            
        Returns:
            邮件内容字符串，如果未找到返回None
        """
        try:
            # 创建IMAP连接
            if port == 993:
                # SSL连接
                mail = imaplib.IMAP4_SSL(imap_server, port)
            else:
                # 普通连接，需要STARTTLS
                mail = imaplib.IMAP4(imap_server, port)
                mail.starttls()
            
            # 登录邮箱
            mail.login(email_address, password)
            
            # 选择收件箱
            mail.select(inbox)
            
            # 搜索所有邮件
            status, messages = mail.search(None, 'ALL')
            
            if status != 'OK':
                return None
            
            # 获取邮件ID列表
            mail_ids = messages[0].split()
            
            if not mail_ids:
                return None
            
            # 从最新的邮件开始查找
            for mail_id in reversed(mail_ids):
                # 获取邮件
                status, msg_data = mail.fetch(mail_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                # 解析邮件
                if not msg_data or not msg_data[0] or len(msg_data[0]) < 2:
                    continue
                raw_email = msg_data[0][1]
                if isinstance(raw_email, (bytes, bytearray)):
                    msg = email.message_from_bytes(raw_email)
                else:
                    continue
                
                # 解码邮件主题
                subject_header = msg.get('Subject', '')
                if subject_header:
                    decoded_subject = decode_header(subject_header)[0]
                    if decoded_subject[1] is not None:
                        subject_str = decoded_subject[0].decode(decoded_subject[1])
                    else:
                        subject_str = str(decoded_subject[0])
                else:
                    subject_str = ""
                
                # 检查主题是否匹配
                if subject.lower() in subject_str.lower():
                    # 获取邮件内容
                    body = EmailTools._get_email_body(msg)
                    
                    # 关闭连接
                    mail.close()
                    mail.logout()
                    
                    return body
            
            # 关闭连接
            mail.close()
            mail.logout()
            
            return None
            
        except Exception as e:
            print(f"获取邮件时出错: {str(e)}")
            return None
    
    @staticmethod
    def _get_email_body(msg) -> str:
        """
        提取邮件正文内容
        
        Args:
            msg: email.message对象
            
        Returns:
            邮件正文字符串
        """
        body = ""
        
        if msg.is_multipart():
            # 处理多部分邮件
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                # 跳过附件
                if "attachment" in content_disposition:
                    continue
                
                # 获取文本内容
                if content_type == "text/plain" or content_type == "text/html":
                    try:
                        body += part.get_payload(decode=True).decode('utf-8')
                    except UnicodeDecodeError:
                        # 尝试其他编码
                        try:
                            body += part.get_payload(decode=True).decode('gb2312')
                        except:
                            body += part.get_payload(decode=True).decode('latin1')
        else:
            # 处理单部分邮件
            try:
                body = msg.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                try:
                    body = msg.get_payload(decode=True).decode('gb2312')
                except:
                    body = msg.get_payload(decode=True).decode('latin1')
        return body.strip()