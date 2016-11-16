from flask_restful import Resource, abort
from flask_restful_swagger.swagger import operation
from flask_jwt import jwt_required
from marshmallow import Schema, fields, post_load, validates, ValidationError

from models.dataset import Dataset

from .analysis import AnalysisSchema
from .stimulus import StimulusSchema

from sqlalchemy.orm.exc import NoResultFound

class DatasetSchema(Schema):
	id = fields.Str(dump_only=True)
	external_id = fields.Str(required=True)
	analyses = fields.Nested(AnalysisSchema, many=True, only='id')
	stimuli = fields.Nested(StimulusSchema, many=True, only='id')
	name = fields.Str(required=True)

	@post_load
	def make_db(self, data):
		return Dataset(**data)

class DatasetResource(Resource):
	""" Individual dataset """
	@operation(
	responseMessages=[{"code": 400,
	      "message": "Dataset does not exist"}])
	@jwt_required()
	def get(self, dataset_id):
		""" Access a specific dataset """
		try:
			result = Dataset.query.filter_by(external_id=dataset_id).one()
			return DatasetSchema().dump(result)
		except NoResultFound:
			abort(400, message="Dataset {} does not exist".format(dataset_id))


class DatasetListResource(Resource):
	""" Available datasets """
	@operation()
	@jwt_required()
	def get(self):
		""" List of datasets """
		result = Dataset.query.filter_by().all()
		return DatasetSchema(many=True).dump(result)
