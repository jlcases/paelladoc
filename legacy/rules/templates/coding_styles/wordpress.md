---
title: "WordPress Development Coding Style Guide"
date: 2025-03-22
author: "PAELLADOC"
version: 1.0
status: "Active"
tags: ["WordPress", "PHP", "CMS", "web development", "themes", "plugins"]
---

# WordPress Development Coding Style Guide

## Project Structure
- Follow WordPress standard directory structure for themes and plugins
- Separate functionality into logical components and files
- Use proper namespacing for plugins to avoid conflicts
- Implement child themes rather than modifying parent themes directly
- Organize template files according to WordPress template hierarchy
- Keep assets (CSS, JS, images) in dedicated directories
- Use includes and partials to avoid code duplication

## PHP Coding Standards
- Follow WordPress PHP Coding Standards
- Use appropriate PHP version based on WordPress requirements
- Properly sanitize, validate, and escape all data
- Implement proper error handling and logging
- Follow naming conventions:
  - Functions: lowercase with underscores
  - Classes: capitalized words
  - Constants: all uppercase with underscores
- Document code with PHPDoc comments
- Properly prefix all functions, classes, and variables in plugins

## Template Structure
- Respect WordPress template hierarchy
- Keep template files focused on presentation logic
- Move complex functionality to separate functions in functions.php or dedicated files
- Use WordPress template tags instead of direct database queries
- Implement proper loop structures with necessary checks
- Use get_template_part() for reusable template sections
- Separate header, footer, and sidebar into appropriate files

## Plugin Development
- Follow WordPress Plugin API best practices
- Use hooks (actions and filters) appropriately instead of modifying core
- Implement activation, deactivation, and uninstall routines
- Create proper admin interfaces that match WordPress UI
- Use WordPress Settings API for configuration options
- Implement nonce verification for form submissions
- Follow WordPress transients API for caching where appropriate
- Create proper uninstall.php file to clean up when plugin is removed

## Theme Development
- Follow WordPress Theme API best practices
- Register and enqueue styles and scripts properly
- Implement theme support for WordPress features
- Build themes that are fully responsive and mobile-friendly
- Use proper translation and localization functions
- Use theme customizer instead of custom options pages when possible
- Implement proper template tags and conditional tags
- Follow accessibility guidelines for themes

## Database Interactions
- Use WordPress database API (wpdb) instead of direct SQL
- Prepare all SQL queries to prevent SQL injection
- Create proper database tables with dbDelta()
- Use appropriate data types and indexing
- Implement proper transactions where needed
- Use post meta, user meta, and options APIs where appropriate
- Follow WordPress caching principles

## JavaScript Standards
- Follow WordPress JavaScript Coding Standards
- Properly enqueue JavaScript files
- Namespace all JavaScript functions and variables
- Implement proper error handling in JavaScript
- Use jQuery or vanilla JS as appropriate
- Follow JavaScript best practices for performance
- Implement proper event handling and delegation
- Use AJAX properly with WordPress REST API or admin-ajax.php

## Security Practices
- Follow WordPress security best practices
- Implement capability checks for all admin functions
- Verify nonces for all form submissions
- Sanitize, validate, and escape all data input/output
- Avoid direct database queries that can be exploited
- Protect sensitive files and directories
- Follow principle of least privilege for users
- Implement proper authentication and authorization

## Performance Optimization
- Optimize database queries and use caching
- Minify and concatenate CSS and JavaScript
- Optimize images and use appropriate formats
- Implement lazy loading for images and other content
- Use appropriate caching mechanisms (object cache, page cache)
- Follow WordPress performance best practices
- Minimize HTTP requests
- Consider using CDN for static assets

## Accessibility
- Follow WCAG 2.1 guidelines at AA level
- Use semantic HTML5 elements
- Implement proper ARIA roles and landmarks
- Ensure keyboard navigation works properly
- Maintain sufficient color contrast
- Provide text alternatives for non-text content
- Ensure forms are accessible
- Test with screen readers and accessibility tools

## WordPress APIs
- Use WordPress REST API for data access when appropriate
- Utilize WordPress Customizer API for theme options
- Implement Shortcode API properly for content extensions
- Use WordPress Settings API for admin options
- Follow WordPress Rewrite API for custom permalinks
- Implement Widget API properly for sidebars and widget areas
- Use Block Editor (Gutenberg) API for modern editing experience
- Leverage WordPress HTTP API for external requests

## Internationalization
- Make all themes and plugins translation-ready
- Use proper translation functions (`__()`, `_e()`, etc.)
- Provide text domain for all translations
- Use translation-ready strings in all user-facing text
- Consider RTL language support in layouts
- Implement number and date formatting for internationalization
- Include translation files or use GlotPress for distribution

## Testing
- Implement unit tests with PHPUnit where appropriate
- Test themes and plugins across multiple browsers
- Verify compatibility with latest WordPress version
- Test with different PHP versions within WordPress requirements
- Implement integration tests for complex functionality
- Test performance under various conditions
- Verify accessibility compliance

## Deployment and Version Control
- Use version control (Git) for all development
- Implement semantic versioning for releases
- Create proper readme.txt files following WordPress format
- Document changes in changelog
- Follow proper deployment practices
- Consider using build tools for production assets
- Implement continuous integration when possible

## Custom Post Types and Taxonomies
- Register CPTs and taxonomies following WordPress best practices
- Use appropriate capabilities for custom post types
- Implement proper labels and messages
- Consider permalink structure and archive pages
- Use appropriate UI elements in admin
- Implement custom metaboxes where needed
- Consider relationships between post types
- Use custom taxonomies for proper content organization 