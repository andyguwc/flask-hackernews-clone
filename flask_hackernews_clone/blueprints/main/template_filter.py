from .views import blueprint
import datetime as dt 

@blueprint.app_template_filter('format_date')
def format_date(ts):
    return ts.strftime('%Y-%m-%d')
