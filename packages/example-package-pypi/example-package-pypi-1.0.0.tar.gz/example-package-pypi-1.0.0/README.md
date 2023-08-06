## 关于 pypi-demo

这是统一制品库 pypi 协议的测试工程，大家可以使用这个工程体验 Python 制品构建、上传和下载。

## 声明

社区在 2022年 1 月 1 日 已不再支持 Python2，这里使用 Python3 演示。 

## 使用方法
### 配置

在本地 ~/.pypirc 文件中写入

```
[pypi]
repository: http://localhost:8888/artifact/repositories/simple/
username: admin
password: adminTest2022
```

本地启动 artifacts 应用后默认监听 8888 端口，默认使用 simple 库。如测试联调环境，请将 localhost 替换成联调环境 ip 即可(下载时命令行参加追加 --trusted-host [联调环境ip])。

### 构建

```python3 -m build```

### 上传

```python3 -m twine upload dist/*```

### 下载

```python3 -m pip download example-pypi-package==0.0.1 -i http://localhost:8888/artifact/repositories/simple/```