import datetime 
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .core.sqlRunner import *
from .core.SqlRunnerThread import *
from .forms import SqlScriptForm
from .forms import RunForm
from .models import SqlScript
from .models import Run


def homepage(request):
    if request.method == "POST":
        print(request.FILES)
        if request.FILES:
            print("Files arrived to the server")
        
        form = SqlScriptForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            sqlscript = form.save(commit=False)
            sqlscript.createdby = request.user
            sqlscript.save()
            return redirect(scripts)
    else:
        form = SqlScriptForm()
    return render(request, "homepage.html", { "form": form })

def scripts(request):
    scripts = SqlScript.objects.all()
    context = { "scripts" : scripts }
    return render(request, "scripts.html", context)

def runs(request):
    run_models = Run.objects.all()
    context = { "run_models": run_models }
    return render(request, "runs.html", context)

def create_run(request, script_id):
    script = SqlScript.objects.get(pk=script_id)
    form = RunForm(initial={script:script})
    context = { "form" : form, "filename" : script.file.name.split('/')[-1] }
    return render(request, "run.html", context)

def run(request, script_id):
    script =  SqlScript.objects.get(pk=script_id)
    if request.method == "POST":
        form = RunForm(request.POST)
       
        if form.is_valid():
            run_model = form.save(commit=False)
            run_model.date = datetime.datetime.now()
            run_model.user = request.user
            run_model.status = "R"
            run_model.script = script
            run_model.save()
            #trigger the script excecution
            run_script(script, run_model)
            #redirect to the list of runs
            return redirect(runs)
        else:
            return render(request, "run.html", { "form": form, "filename": script.get_file_name() })
    
    form = RunForm()
    return render(request, "run.html", { "form": form, "filename": script.get_file_name() })

def run_script(script, run_model):
    
    def success(context):
        if context:
            run_id = context["runid"]
            rmodel = Run.objects.get(pk=run_id)
            rmodel.status = "S"
            rmodel.save()

    def failed(context):
        if context:
            run_id = context["runid"]
            rmodel = Run.objects.get(pk=run_id)
            rmodel.status = "F"
            rmodel.save()
    
    sql = script.file.read()
    conn_strings = list(map(str.strip, run_model.connstrings.split('\n')))
    thread_count = 1
    threads = []
    for conn_string in conn_strings:
        sql_runner = SqlRunner.from_sql_server_connection_string(conn_string)
        runner_thread = SqlRunnerThread.from_sqlrunner(sql_runner, sql, "thread-%d" % thread_count,
            "thread-%d" % thread_count,thread_count)
        threads.append(runner_thread)
        runner_thread.success_function = success
        runner_thread.failed_function = failed
        runner_thread.context = { "runid": run_model.id }
        runner_thread.start()
    
