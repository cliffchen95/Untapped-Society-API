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
    photo=payload['photo'],
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

## companies/delete
## Company delete route
@companies.route('delete/<id>', methods=['DELETE'])
@login_required
def delete_company(id):
  try:
    company_info = CompanyInfo.get_by_id(id)
    company_info_dict = model_to_dict(company_info)

    ## the current user is the admin of the company
    if company_info_dict['user']['id'] == current_user.id:
      ## delete the company info
      company_info.delete_instance()
      return jsonify(
        data={},
        message=f"Deleted company with name {company_info_dict['name']}",
        status=200
      ), 200

    else:
      return jsonify(
        data={},
        message=f"The current user does not have permission to delete the company info",
        status=403
      ), 403

  except models.DoesNotExist:
    return jsonify(
      data={},
      message=f"Company with id {id} does not exist",
      status=401
    ), 401

## companies/update
## Company info update
@companies.route('/update/<id>', methods=['PATCH'])
@login_required
def update_company(id):
  payload = request.get_json()
  try:
    company_info = CompanyInfo.get_by_id(id)
    company_info_dict = model_to_dict(company_info)

    ## the current user is the admin of the company
    if company_info_dict['user']['id'] == current_user.id:
      ## update the company info
      CompanyInfo.update(payload).where(
        CompanyInfo.id == id).execute()
      company_info = CompanyInfo.get_by_id(id)
      company_info_dict = model_to_dict(company_info)
      company_info_dict['user'].pop('password')

      return jsonify(
        data={"updated_company": company_info_dict},
        message=f"Updated company with name {company_info_dict['name']}",
        status=200
      ), 200

    else:
      return jsonify(
        data={},
        message=f"The current user does not have permission to update the company info",
        status=403
      ), 403    
  except models.DoesNotExist:
    return jsonify(
      data={},
      message=f"Company with id {id} does not exist",
      status=401
    ), 401

## companies/<id>
## Get company info with <id>
@companies.route('/<id>', methods=['GET'])
@login_required
def get_company(id):
  try:
    company_info = CompanyInfo.get_by_id(id)
    job_postings_query = company_info.Posting
    job_posts = []
    for job_post in job_postings_query:
      job_post = model_to_dict(job_post)
      job_post.pop('company')
      job_posts.append(job_post)
      
    company_info_dict = model_to_dict(company_info)
    company_info_dict['user'].pop('password')
    company_info_dict['jobposts'] = job_posts
    return jsonify(
      data={"company": company_info_dict},
      message=f"Successfully found company with id {id}",
      status=200
    ), 200
  except models.DoesNotExist:
    return jsonify(
      data={},
      message="Invalid id",
      status=404
      ), 404

## /companies/search
## look for company by name, retun a list of company with name contain the search
## query, results only contains id and name
@companies.route('/search', methods=['GET'])
@login_required
def search_company():
  query = request.args.get('query')
  print(query)
  if query == "":
    return jsonify(
      data={},
      message="No search query provide",
      status=204
      ), 204
  try:
    companies = (
      CompanyInfo.select(CompanyInfo.id, CompanyInfo.name)
      .where(CompanyInfo.name.contains(query))
      )
    ## only get the id and the name from search results
    companies = [model_to_dict(company, fields_from_query=companies) for company in companies]

    return jsonify(
      data=companies,
      message=f"Successfully found {len(companies)}",
      status=200
      ), 200

  except models.DoesNotExist:
    return jsonify(
      data={},
      message="No company found",
      status= 204
      ), 204

