
# flask api tool [flaspi]

import sys
import json
import flask

# create post api [flaspi]
def post_api(path, api_func, app):
	# 関数の登録
	@app.route(path, methods = ["post"])
	def temporary_func():
		# リクエストをjson形式で受け取り
		request_obj = flask.request.json
		# 処理の実行
		response_obj = api_func(request_obj)
		# 返却されたオブジェクトをjson形式にして返す
		try:
			response_json = json.dumps(response_obj, ensure_ascii = False, indent = 2)
			return response_json
		except:
			# jsonフォーマットに則っていない場合
			return "invalid_response_json_format", 500
