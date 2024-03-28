FROM node:18-alpine as frontend-builder

COPY ./ui/web/frontend /app

RUN cd /app && yarn install && yarn build


FROM djvue/urfu-deployments:pi2-base-cpu-tiny as final

WORKDIR /app

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/_info

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

COPY --from=frontend-builder /app/dist /app/ui/web/frontend/dist

RUN cp /OpenFace/lib/local/LandmarkDetector/model/patch_experts/* /OpenFace/build/bin/model/patch_experts/

ENTRYPOINT ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]