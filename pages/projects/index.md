---
layout: default
title: Projects
description: Browse documentation for all PAELLADOC projects
permalink: /projects/
---

<div class="projects-container">
  <div class="projects-header">
    <div class="search-container">
      <input type="text" id="projectSearch" placeholder="Search projects..." class="search-input">
      <div class="filter-tags">
        <button class="tag-filter active" data-tag="all">All</button>
        <button class="tag-filter" data-tag="web">Web</button>
        <button class="tag-filter" data-tag="mobile">Mobile</button>
        <button class="tag-filter" data-tag="api">API</button>
        <button class="tag-filter" data-tag="desktop">Desktop</button>
      </div>
    </div>
  </div>

  <div class="projects-grid" id="projectsGrid">
    {% assign project_dirs = site.pages | where_exp: "item", "item.path contains 'projects/'" | where_exp: "item", "item.path != 'projects/index.md'" %}
    {% assign unique_projects = "" | split: "," %}
    
    {% for page in project_dirs %}
      {% assign path_parts = page.path | split: "/" %}
      {% if path_parts.size > 1 %}
        {% assign project_name = path_parts[1] %}
        {% unless unique_projects contains project_name %}
          {% assign unique_projects = unique_projects | push: project_name %}
        {% endunless %}
      {% endif %}
    {% endfor %}
    
    {% for project_name in unique_projects %}
      {% if project_name != "RECUENCO" and project_name != "MALENIO" %}
        {% assign project_index = site.pages | where_exp: "item", "item.path contains project_name" | where_exp: "item", "item.name contains 'index.md'" | first %}
        {% if project_index %}
          <div class="project-card" data-tags="{{ project_index.tags | join: ' ' | default: 'general' }}">
            <div class="project-header">
              <h3 class="project-title">{{ project_name }}</h3>
              <div class="project-tags">
                {% assign project_tags = project_index.tags | default: "general" %}
                {% for tag in project_tags %}
                  <span class="tag">{{ tag }}</span>
                {% endfor %}
              </div>
            </div>
            <p class="project-description">{{ project_index.description | default: project_index.excerpt | strip_html | truncate: 120 }}</p>
            <div class="project-footer">
              <a href="{{ project_index.url }}" class="project-link">View Project</a>
              <span class="project-date">{{ project_index.date | date: "%m/%d/%Y" }}</span>
            </div>
          </div>
        {% endif %}
      {% endif %}
    {% endfor %}
  </div>
  
  {% assign public_project_count = 0 %}
  {% for project_name in unique_projects %}
    {% if project_name != "RECUENCO" and project_name != "MALENIO" %}
      {% assign public_project_count = public_project_count | plus: 1 %}
    {% endif %}
  {% endfor %}
  
  {% if public_project_count == 0 %}
    <div class="no-projects">
      <p>No public projects available at this time.</p>
    </div>
  {% endif %}
</div>

<style>
  .projects-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .projects-header {
    margin-bottom: 30px;
    text-align: center;
  }
  
  .search-container {
    margin: 20px 0;
  }
  
  .search-input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    margin-bottom: 15px;
  }
  
  .filter-tags {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .tag-filter {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 8px 15px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .tag-filter.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
  }
  
  .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .project-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    background-color: white;
    display: flex;
    flex-direction: column;
  }
  
  .project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  }
  
  .project-header {
    padding: 15px;
    border-bottom: 1px solid #eee;
  }
  
  .project-title {
    margin: 0 0 10px 0;
    font-size: 18px;
  }
  
  .project-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }
  
  .tag {
    background-color: #f0f0f0;
    color: #666;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 12px;
  }
  
  .project-description {
    padding: 15px;
    flex-grow: 1;
    color: #666;
    font-size: 14px;
  }
  
  .project-footer {
    padding: 15px;
    border-top: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .project-link {
    background-color: var(--primary-color);
    color: white;
    padding: 8px 15px;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.3s ease;
  }
  
  .project-link:hover {
    background-color: #c94d1c;
    text-decoration: none;
  }
  
  .project-date {
    color: #999;
    font-size: 12px;
  }
  
  .no-projects {
    text-align: center;
    padding: 40px;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin-top: 20px;
  }
  
  @media (max-width: 768px) {
    .projects-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('projectSearch');
    const projectCards = document.querySelectorAll('.project-card');
    const tagFilters = document.querySelectorAll('.tag-filter');
    
    // Search functionality
    searchInput.addEventListener('input', filterProjects);
    
    // Tag filtering
    tagFilters.forEach(button => {
      button.addEventListener('click', function() {
        tagFilters.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        filterProjects();
      });
    });
    
    function filterProjects() {
      const searchTerm = searchInput.value.toLowerCase();
      const activeTag = document.querySelector('.tag-filter.active').getAttribute('data-tag');
      
      projectCards.forEach(card => {
        const title = card.querySelector('.project-title').textContent.toLowerCase();
        const description = card.querySelector('.project-description').textContent.toLowerCase();
        const tags = card.getAttribute('data-tags').toLowerCase();
        
        const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
        const matchesTag = activeTag === 'all' || tags.includes(activeTag);
        
        if (matchesSearch && matchesTag) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }
  });
</script>