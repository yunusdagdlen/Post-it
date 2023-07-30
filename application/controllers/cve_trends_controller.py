from flask import render_template, abort, make_response

from application.controller import mod_pages
from application.utils.cve_trends_utils import CveTrendsUtils


@mod_pages.route('/')
def cve():
    response = CveTrendsUtils.GetCveUtils()

    # if response:
    #     ""
    # else:
    #     abort(make_response("Not Found", 404))

    return render_template('cve_trends.html', cveItems=response)