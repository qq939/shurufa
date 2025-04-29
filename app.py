from flask import Flask, redirect, render_template, request
import yaml

from shurufatools import aitools

app = Flask(__name__)
# 将 enumerate 函数添加到 Jinja2 环境中
app.jinja_env.globals.update(enumerate=enumerate)
with open('config.yaml', 'r', encoding="utf-8") as f:
    config = yaml.safe_load(f)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 加载配置文件
    with open('config.yaml', 'r', encoding="utf-8") as f:
        config = yaml.safe_load(f)
    result = None
    task_index = 0
    global task_keys
    task_keys = ["".join(i.keys()) for i in config["tasks"]]  # 获取 tasks 里的键
    print(task_keys)
    if request.method == 'POST':
        task_index_str = request.form.get('selected_task_index')
        if task_index_str:
            task_index = int(task_index_str)
        else:
            print("selected_task_index is None")
        input_text = request.form.get('input_text')
        result = aitools().implement(input_text, task_index)

    return render_template('index.html', result=result, task_keys=task_keys)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    global task_keys 
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
    else:
        task_name = ''
        task_description = ''
    if task_name and task_description:
        # 检查任务名称是否已存在
        with open('config.yaml', 'r', encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        task_keys = ["".join(i.keys()) for i in config["tasks"]]  
        if task_name in task_keys:
            # 更新任务描述
            for task in config["tasks"]:
                if task_name in task:
                    task[task_name] = task_description
                    break
        else:
            # 添加新任务
            config["tasks"].append({task_name: task_description})
            task_keys.append(task_name)
        with open('config.yaml', 'w', encoding="utf-8") as f:
            yaml.dump(config, f)
        return redirect('/')
    return render_template('add_task.html', task_name=task_name, task_description=task_description)

@app.route('/delete_task/<int:index>', methods=['POST'])
def delete_task(index):
    global task_keys  # 假设 task_keys 是全局变量
    # 加载配置文件
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print(config["tasks"])
    if 0 <= index <= len(config["tasks"]):
        
        # 删除指定索引的任务
        del config["tasks"][index]
        task_keys = ["".join(i.keys()) for i in config["tasks"]]  # 更新 task_keys
        # 保存修改后的配置文件
        with open('config.yaml', 'w', encoding="utf-8") as f:
            yaml.dump(config, f)
        return redirect('/')
    else:
        return '无效的任务索引', 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['port'], debug=True)
 