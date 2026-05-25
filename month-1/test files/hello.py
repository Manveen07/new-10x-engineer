import modal

image = modal.Image.debian_slim().pip_install("fastapi[standard]")
app = modal.App("hello-world", image=image)


@app.function()
@modal.fastapi_endpoint()
def hello():
    return {"message": "hello from modal"}
