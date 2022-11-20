from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import FormView, TemplateView
from . import forms
from . import view_finance

# Create your views here.
def IndexView(request):
    return render(request, 'index.html')

class PlotView(TemplateView):

    template_name = 'plot.html'

    # def a(request):


    #     get = request.GET
  
    #     search = get.get('id_search')

    #     print(search)


    #変数としてグラフイメージをテンプレートに渡す
    def get_context_data(self, **kwargs):
        request = self.request

        get = request.GET
  
        search = get.get('search')

  
        # search = '^N225'

        
        chart = view_finance.Plot_Graph(search)          #グラフ作成

        # chart = view_finance.out(search)

        #変数を渡す
        context = super().get_context_data(**kwargs)
        context['chart'] = chart
        return context

    #get処理
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)