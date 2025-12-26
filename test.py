import os

# Nếu nó in ra đường dẫn ổ D là thành công
print(f"Nhà mới của AI: {os.getenv('HF_HOME')}")

# Test thử tải một model siêu nhỏ (dummy) xem nó chui vào đâu
from huggingface_hub import snapshot_download

snapshot_download(repo_id="prajjwal1/bert-tiny")
# Sau khi chạy xong, ông vào ổ D kiểm tra xem có thêm file mới không.
