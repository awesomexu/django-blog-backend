## 基于django的简易博客后端api

### API接口：
| url            | method | example                                       |
| -------------- | ------ | --------------------------------------------- |
| `user/reg`     | `POST` | `http://127.0.0.1:8000/user/reg/`             |
| `user/login`   | `POST` | `http://127.0.0.1:8000/user/login/`           |
| `user/publish` | `POST` | `http://127.0.0.1:8000/posts/publish/`        |
| `posts/`       | `GET`  | `http://127.0.0.1:8000/posts/?page=1&size=10` |
| `posts/1`      | `GET`  | `http://127.0.0.1:8000/posts/2`               |

