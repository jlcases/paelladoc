---
layout: default
title: About PAELLADOC
description: Learn more about the PAELLADOC interactive documentation system
---

<div class="about-container">
  <div class="about-header">
    <div class="paella-icon">🥘</div>
    <h1>About PAELLADOC</h1>
  </div>

  <div class="about-content">
    <section class="about-section">
      <h2>What is PAELLADOC?</h2>
      <p>PAELLADOC is an interactive documentation system that bridges the gap between product and engineering teams. Just like a perfect paella requires the right combination of ingredients, heat, expertise, and a time-tested recipe, successful product development needs the right mix of tools, pressure, expertise, and documentation.</p>
      
      <p>Our name and philosophy are inspired by the Spanish dish paella - a complex, beautiful creation that requires both art and science to perfect. Like a master chef preparing paella, PAELLADOC helps teams create products that are greater than the sum of their parts.</p>
    </section>

    <section class="about-section">
      <h2>The Paella Philosophy</h2>
      <div class="paella-philosophy">
        <div class="philosophy-item">
          <h3>🍚 Quality Ingredients</h3>
          <p>Just as a paella requires the finest rice, seafood, and saffron, great products need quality components, frameworks, and libraries.</p>
        </div>
        
        <div class="philosophy-item">
          <h3>🔥 Perfect Heat</h3>
          <p>Like the carefully controlled fire under a paella pan, development needs the right amount of pressure - not too much, not too little.</p>
        </div>
        
        <div class="philosophy-item">
          <h3>👨‍🍳 Master Expertise</h3>
          <p>A paella chef knows exactly when to add each ingredient and how long to cook. Similarly, experienced developers know how to structure code and when to refactor.</p>
        </div>
        
        <div class="philosophy-item">
          <h3>📋 Trusted Recipe</h3>
          <p>Even the best chef follows a recipe. PAELLADOC provides the documentation "recipe" that guides teams through complex development processes.</p>
        </div>
      </div>
    </section>

    <section class="about-section">
      <h2>Our Mission</h2>
      <p>PAELLADOC aims to transform how teams document their products and processes. We believe that documentation should be:</p>
      <ul class="mission-list">
        <li><strong>Interactive</strong> - Not static files, but living documents</li>
        <li><strong>Collaborative</strong> - Created by both product and engineering teams</li>
        <li><strong>Accessible</strong> - Easy to create, update, and understand</li>
        <li><strong>Actionable</strong> - Directly connected to development workflows</li>
      </ul>
    </section>

    <section class="about-section">
      <h2>The Team</h2>
      <p>PAELLADOC fue creado por un CPTO que se llama @PR. Como un maestro chef de paella, ha combinado su experiencia y visión para crear algo que es mayor que la suma de sus partes.</p>
    </section>
  </div>
</div>

<style>
  .about-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .about-header {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .paella-icon {
    font-size: 6rem;
    margin-bottom: 1rem;
    animation: steam 3s ease-in-out infinite;
  }
  
  @keyframes steam {
    0% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(5deg); }
    100% { transform: translateY(0) rotate(0deg); }
  }
  
  .about-section {
    margin-bottom: 3rem;
  }
  
  .paella-philosophy {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 1.5rem;
  }
  
  .philosophy-item {
    background-color: var(--gray-50);
    border-radius: var(--border-radius-md);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .philosophy-item:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-md);
  }
  
  .philosophy-item h3 {
    color: var(--paella-orange);
    margin-top: 0;
    margin-bottom: 1rem;
  }
  
  .mission-list {
    list-style-type: none;
    padding-left: 0;
  }
  
  .mission-list li {
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--gray-200);
  }
  
  .mission-list li:last-child {
    border-bottom: none;
  }
  
  @media (max-width: 768px) {
    .paella-philosophy {
      grid-template-columns: 1fr;
    }
  }
</style> 