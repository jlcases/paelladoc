#!/usr/bin/env python3
import os
import re


def update_references_in_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Actualizar referencias a ProjectMetadata por ProjectInfo
    content = re.sub(r"Metadata as ProjectMetadata", "ProjectInfo", content)
    content = re.sub(r"ProjectMetadata", "ProjectInfo", content)

    # 2. Actualizar referencias a metadata por project_info
    content = re.sub(r"\.metadata\.", ".project_info.", content)
    content = re.sub(r"memory\.metadata", "memory.project_info", content)
    content = re.sub(
        r"original_memory\.metadata", "original_memory.project_info", content
    )
    content = re.sub(r"project\.metadata", "project.project_info", content)

    with open(file_path, "w") as f:
        f.write(content)

    print(f"Actualizado: {file_path}")


def find_and_update_test_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                update_references_in_file(file_path)


if __name__ == "__main__":
    find_and_update_test_files("tests")
    # También actualizar los adaptadores
    find_and_update_test_files("paelladoc/adapters")
