{{- define "pilot.name" -}}{{ .Release.Name }}-{{ .svc }}{{- end -}}
{{- define "pilot.labels" -}}
app.kubernetes.io/name: {{ .svc }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/part-of: pilot
{{- end -}}
