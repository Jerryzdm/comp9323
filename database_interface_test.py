from interface_database import *




print(interface_target_type_table.insert('living'))
print(interface_target_type_table.select_all())
print(interface_target_type_table.select(["targetID"],["targetname='%s'"%'living']))



print(interface_user_table.insert('student','diming','12345','z@gmail.com','postgraduate'))
print(interface_user_table.select_all())
print(interface_user_table.update(["password='%s'"%'54321'],["username='%s'"%'diming']))
print(interface_user_table.unactived(["userID=1"]))
print(interface_user_table.select([],["username='%s'"%'diming']))


print(interface_post_table.insert('where can i find food?','food','living','diming'))
print(interface_post_table.select_all())
print(interface_post_table.update(["post_content='where can i find food in UNSW?'"],["postID=%d"%1]))
print(interface_post_table.unactived(["postID=1"]))
print(interface_post_table.select(["post_content"],["userID=%d"%1]))


interface_post_reply_table.insert('reply_content',1,1)
print(interface_post_reply_table.select_all())
print(interface_post_reply_table.update(["reply_content='in subway'"],["replyid=%d"%1]))
print(interface_post_reply_table.unactived(["replyid=1"]))
print(interface_post_reply_table.select([],["userID=1"]))
