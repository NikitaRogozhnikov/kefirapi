from flask_restful import reqparse
from datetime import datetime

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True, help='The user\'s email', )
login_parser.add_argument('password', required=True, help='The user\'s password')

base_user_parser = reqparse.RequestParser(bundle_errors=True)
base_user_parser.add_argument('first_name', required=True, help='The user\'s first_name')
base_user_parser.add_argument('last_name', required=True, help='The user\'s last_name')
base_user_parser.add_argument('email', required=True, help='The user\'s email')

post_parser = base_user_parser.copy()
post_parser.add_argument('password', required=True, help='The user\'s password')


private_user_parser = reqparse.RequestParser()
private_user_parser.add_argument('first_name', help='The user\'s first_name')
private_user_parser.add_argument('last_name', help='The user\'s last_name')
private_user_parser.add_argument('email', )
private_user_parser.add_argument('other_name')
private_user_parser.add_argument('password')
private_user_parser.add_argument('birthday', type=datetime)
private_user_parser.add_argument('phone')
private_user_parser.add_argument('is_admin', type=bool)

