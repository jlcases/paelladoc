import re

# Leer el archivo
with open("project.py", "r") as f:
    content = f.read()

# Cambiar nombre de clase Metadata a ProjectInfo para evitar palabras reservadas
content = re.sub(
    r"class ProjectMetadata\(BaseModel\):", "class ProjectInfo(BaseModel):", content
)

# Cambiar referencias a project_metadata para usar project_info
content = re.sub(
    r"project_metadata: ProjectMetadata", "project_info: ProjectInfo", content
)

# Asegurarse de usar project_info en lugar de metadata en todo el código
content = re.sub(r"memory\.metadata\.", "memory.project_info.", content)
content = re.sub(r"self\.metadata\.", "self.project_info.", content)

# Corregir timestamps utcnow()
content = content.replace(
    "datetime.utcnow()", "datetime.datetime.now(datetime.timezone.utc)"
)

# Guardar el archivo modificado
with open("project.py", "w") as f:
    f.write(content)

print("Modificación completada correctamente")
