import axios from "axios";
import config from "./env.json"

let env: any = {}
if (import.meta.env.PROD) {
    env = config.prod
} else {
    env = config.dev
}

class ApiClient {
  private baseUrl = env.apiUrl

  public post = (url: string, data: any) => {
    axios.post(`${this.baseUrl}/${url}`, data);
  }
}

export default ApiClient