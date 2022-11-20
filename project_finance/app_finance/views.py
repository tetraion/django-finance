
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView
from matplotlib.style import context
from requests import request
from . import forms
from . import view_finance
from . import models
from . import graph


class IndexView(FormView):
    form_class = forms.TextForm
    template_name = 'index.html'
    success_url = reverse_lazy('plot')


    def form_valid(self, form, **kwargs):
        request = self.request

        code = form.cleaned_data['code']
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        if request.method == 'POST':
            if "nomal" in request.POST:
                button = 1
            elif "nomal2"  in request.POST:
                button = 2
            elif "nomal3"  in request.POST:
                button = 3

        models.Stock.objects.create(
            code=code,
            start=start,
            end=end,
            button=button,
        )
        return super().form_valid(form)

        



class PlotView(TemplateView):

    template_name = 'plot.html'


    #変数としてグラフイメージをテンプレートに渡す
    def get_context_data(self, **kwargs):

        search = models.Stock.objects.latest("created").code
        start = models.Stock.objects.latest("created").start
        end = models.Stock.objects.latest("created").end

        if models.Stock.objects.latest("created").button == 1:
            chart = view_finance.Plot_Graph(search, start, end)    #グラフ作成
        elif models.Stock.objects.latest("created").button == 2:
            chart = view_finance.candle(search, start, end)
        elif models.Stock.objects.latest("created").button == 3:
            chart,score = view_finance.zyukaiki(search, start, end)

        #変数を渡す
        context = super().get_context_data(**kwargs)
        context['chart'] = chart
        # context['score'] = score
        #context['search']= search
        return context

    #get処理
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# from django.shortcuts import redirect
# class HistoryView(ListView):
#     template_name = "history.html"

#     queryset = models.Stock.objects.all()


def history(request):
    lists = models.Stock.objects.all()
    params = { 'lists': lists}
    return render(request,'history.html',params)  # 一覧ページにリダイレクト