import json
from io import BytesIO

import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from robots.forms import RobotForm
from robots.models import Robot


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RobotForm(data)

            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Robot information saved successfully'})
            else:
                return JsonResponse({'error': form.errors.as_json()}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


class GenerateReportView(View):
    def get(self, request, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=7)
        robots = Robot.objects.filter(created__range=(start_date, end_date))

        # Create DataFrame
        df = self.create_dataframe(robots)

        # Group and create model DataFrames
        model_dfs = self.group_data_by_model(df)

        # Create Excel and send response
        response = self.create_excel_response(model_dfs)

        return response

    def create_dataframe(self, robots):
        data = {
            'Model': [robot.model for robot in robots],
            'Version': [robot.version for robot in robots]
        }
        return pd.DataFrame(data)

    def group_data_by_model(self, df):
        grouped_df = df.groupby(['Model', 'Version']).size().reset_index(name='Количество за неделю')
        model_dfs = {}
        for model in grouped_df['Model'].unique():
            model_data = grouped_df[grouped_df['Model'] == model].copy()
            model_data.set_index('Version', inplace=True)
            model_dfs[model] = model_data
        return model_dfs

    def create_excel_response(self, model_dfs):
        output = BytesIO()
        with pd.ExcelWriter(output) as writer:
            for model, model_data in model_dfs.items():
                model_data.to_excel(writer, sheet_name=model)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=robot_summary.xlsx'
        response.write(output.getvalue())

        return response