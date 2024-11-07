import pymongo
from cfg import mongo_url
from bson.objectid import ObjectId
myclient = pymongo.MongoClient(mongo_url)
mydb = myclient["vn-newsflow"]

mycol = mydb["chatroles"]



def find_by_id( object_id):
  """
  Tìm kiếm một tài liệu trong một collection dựa trên ObjectId.

  Args:
    collection: Đối tượng Collection trong MongoDB.
    object_id: Chuỗi chứa ObjectId.

  Returns:
    Tài liệu được tìm thấy, hoặc None nếu không tìm thấy.
  """
  myquery = { "_id": ObjectId(object_id) }
  mydoc = mycol.find_one(myquery)
  return mydoc

def get_prompt_comment(role_id):
    """
    Lấy ra prompt của role từ database

    Args:
        role_id (string): id của role

    Returns:
        string: prompt của role
    """
    roles = find_by_id(role_id)
    return roles["promptComment"]