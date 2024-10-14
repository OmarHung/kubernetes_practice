# ConfigMap

## 建立 ConfigMap
用檔案建構
```bash
kubectl create configmap test-config --from-file=path/to/config.yaml
```

用檔案建構並指定 key
```bash
kubectl create configmap test-config --from-file=app.properties=path/to/config.yaml
``` 

用資料夾建構，資料夾內的檔案會被視為 key-value pair
```bash
kubectl create configmap test-config --from-file=config/
```

用 key-value pair 建構
```bash
kubectl create configmap test-config --from-literal=APP_NAME=fastapi --from-literal=APP_VERSION=0.1
```

## 用 ConfigMap 設定環境變數
建立 pod 時，可以使用 ConfigMap 的 key 來設定環境變數
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-env-cm
spec:
  containers:
    - name: env-test
      image: alpine
      command: ["/bin/sh", "-c", "env; sleep 3600"]
      imagePullPolicy: IfNotPresent
      restartPolicy: Never
      env:
        - name: APP_NAME # 環境變數名稱
          valueFrom:
            configMapKeyRef:
              name: test-config # ConfigMap 名稱
              key: APP_NAME # ConfigMap 的 key
        - name: APP_VERSION
          valueFrom:
            configMapKeyRef:
              name: test-config
              key: APP_VERSION
```
建立 pod
```bash
kubectl create -f configmap-pod01.yaml
```

查看日誌
```bash
kubectl logs test-env-cm
```

## 用 ConfigMap 設定 Volume
建立config內的設定文件
db.yaml
```yaml
host: mongodb
port: 27017
```

redis.properties
```properties
host=redis
port=6379
```

建立 ConfigMap
```bash
kubectl create configmap test-dir-config --from-file=config/
```

建立 pod 時，可以使用 ConfigMap 的 key 來設定 Volume
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-volume-cm
spec:
  containers:
    - name: volume-cm-test
      image: alpine
      command: ["/bin/sh", "-c", "sleep 3600"]
      imagePullPolicy: IfNotPresent
      volumeMounts: # 掛載 volume
        - name: config-volume # volume 名稱
          mountPath: /etc/config # 掛載路徑
  volumes:
    - name: config-volume # volume 名稱
      configMap: # 使用 ConfigMap
        name: test-dir-config # ConfigMap 名稱
        items: # 指定要使用的檔案
          - key: db.yaml # ConfigMap 的 key
            path: db.yaml # 掛載路徑
  restartPolicy: Never
```

建立 pod
```bash
kubectl create -f configmap-pod02.yaml
```

進入 pod 查看
```bash
kubectl exec -it test-volume-cm -- /bin/sh

cd /etc/config

cat db.yaml
```

