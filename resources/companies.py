import models

CompanyInfo = models.CompanyInfo

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

companies = Blueprint('companies', 'companies')

## companies/create
## Create new company
@companies.route('/create', methods=['POST'])
@login_required
def create_company():
  payload = request.get_json()
  company = CompanyInfo.create(
    user=current_user.id,
    name=payload['name'],
    description=payload['description'],
    tagline=payload['tagline'],
    address=payload['address'],
    industry=payload['industry'],
    website=payload['website'],
    linkedin=payload['linkedin'],
    twitter=payload['twitter'],
    github=payload['github'],
    facebook=payload['facebook'],
    instagram=payload['instagram'],
    pinterest=payload['pinterest'],
    youtube=payload['youtube']
  )
  company_dict = model_to_dict(company)
  company_dict['user'].pop('password')

  return jsonify(
    data={"company": company_dict},
    message=f"Successfully set up company for with name {company_dict['name']}",
    status=201
  ), 201