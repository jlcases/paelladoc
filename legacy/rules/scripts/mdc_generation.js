/**
 * MDC Generation Module
 * This module handles generating MDC files that act as orchestrators
 * for project development based on documentation.
 */

const fs = require('fs');
const path = require('path');

/**
 * Generates an MDC file based on project documentation
 * 
 * @param {Object} options - Generation options
 * @param {string} options.projectName - Project name
 * @param {string} options.outputPath - Output path for the MDC file
 * @param {string} options.filename - MDC filename
 * @param {Object} options.developmentInfo - Development information extracted
 * @returns {Object} Generation result
 */
function generateMDC(options) {
  const {
    projectName,
    outputPath,
    filename,
    developmentInfo
  } = options;
  
  // Ensure filename has .example extension
  const finalFilename = ensureExampleExtension(filename || `${projectName}.mdc.example`);
  
  // Ensure the output directory exists
  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
  }
  
  // Get list of available documentation files - ONLY from the project folder
  const docsPath = path.join('docs', projectName);
  let availableDocs = [];
  
  if (fs.existsSync(docsPath)) {
    availableDocs = fs.readdirSync(docsPath)
      .filter(file => file.endsWith('.md'))
      .map(file => ({
        filename: file,
        path: `docs/${projectName}/${file}`,
        type: getDocumentType(file),
        description: getDocumentDescription(file)
      }));
  }
  
  // Start building the MDC content - extremely lightweight
  let mdcContent = `description: "${projectName} - ${developmentInfo && developmentInfo.description ? developmentInfo.description : `Proyecto documentado con PAELLADOC`}"\n`;
  mdcContent += `globs: ["**/*"]\n`;
  mdcContent += `alwaysApply: true\n`;
  
  // Only add instruction sections if we have relevant documents
  if (availableDocs.length > 0) {
    mdcContent += `instructions:\n`;
    
    // Check if index document exists
    const indexDoc = availableDocs.find(d => d.filename === '00_index.md');
    if (indexDoc) {
      mdcContent += `  global_architecture: |\n`;
      mdcContent += `    # Arquitectura Global de ${projectName}\n`;
      mdcContent += `    \n`;
      mdcContent += `    Consultar ${indexDoc.path} para la arquitectura completa del proyecto.\n\n`;
    }
    
    // Check if quick_task_documentation exists
    const taskDoc = availableDocs.find(d => d.filename === 'quick_task_documentation.md');
    if (taskDoc) {
      mdcContent += `  code_standards: |\n`;
      mdcContent += `    # Estándares de Código\n`;
      mdcContent += `    \n`;
      mdcContent += `    Para información sobre estándares de código y mejores prácticas, consultar:\n`;
      mdcContent += `    ${taskDoc.path}\n\n`;
    }
    
    // Add patterns section only for documents that exist
    mdcContent += `patterns:\n`;
    
    // Add feature documentation pattern if it exists
    const featureDoc = availableDocs.find(d => d.filename === 'feature_documentation.md');
    if (featureDoc) {
      mdcContent += `  - name: "Componentes Principales"\n`;
      mdcContent += `    pattern: "src/**/*"\n`;
      mdcContent += `    instructions: |\n`;
      mdcContent += `      # Componentes Principales\n`;
      mdcContent += `      \n`;
      mdcContent += `      Consultar ${featureDoc.path} para detalles de implementación.\n\n`;
    }
    
    // Add bug documentation pattern if it exists
    const bugDoc = availableDocs.find(d => d.filename === 'bug_documentation.md');
    if (bugDoc) {
      mdcContent += `  - name: "Pruebas y Calidad"\n`;
      mdcContent += `    pattern: "**/*.test.*"\n`;
      mdcContent += `    instructions: |\n`;
      mdcContent += `      # Pruebas y Errores\n`;
      mdcContent += `      \n`;
      mdcContent += `      Seguir el proceso de documentación de errores definido en:\n${bugDoc.path}\n\n`;
    }
  }
  
  // Add a simple rules section referencing only existing documents
  mdcContent += `rules:\n`;
  mdcContent += `  - name: "${projectName}-rules"\n`;
  mdcContent += `    description: "Reglas de desarrollo para ${projectName}"\n`;
  mdcContent += `    patterns: ["**/*"]\n`;
  mdcContent += `    instructions:\n`;
  mdcContent += `      - "# ${projectName} - Reglas de Desarrollo"\n`;
  
  // Only add docs section if we have documents
  if (availableDocs.length > 0) {
    mdcContent += `      - ""\n`;
    mdcContent += `      - "## Documentación Disponible"\n`;
    mdcContent += `      - "La documentación está disponible en docs/${projectName}/"\n`;
    mdcContent += `      - ""\n`;
    mdcContent += `      - "## Documentos del Proyecto"\n`;
    
    // List only available project docs
    availableDocs.forEach(doc => {
      mdcContent += `      - "- ${doc.path} - ${doc.description}"\n`;
    });
  } else {
    mdcContent += `      - ""\n`;
    mdcContent += `      - "## Advertencia"\n`;
    mdcContent += `      - "No se encontraron documentos en docs/${projectName}/"\n`;
  }
  
  // Add references section only for existing docs
  if (availableDocs.length > 0) {
    mdcContent += `\nreferences:\n`;
    availableDocs.forEach(doc => {
      mdcContent += `  - "${doc.path}"\n`;
    });
  }
  
  // Save the MDC file
  const mdcPath = path.join(outputPath, finalFilename);
  fs.writeFileSync(mdcPath, mdcContent, 'utf8');
  
  // Return information about the generated file
  return {
    file_path: mdcPath,
    rule_count: 1, // Just one rule
    pattern_count: (featureDoc ? 1 : 0) + (bugDoc ? 1 : 0), // Count existing patterns
    instruction_count: availableDocs.length > 0 ? 2 : 0, // Architecture + Code standards if docs exist
    doc_count: availableDocs.length
  };
}

/**
 * Ensures the filename has the .example extension
 */
function ensureExampleExtension(filename) {
  if (!filename.endsWith('.example')) {
    // If filename already has .mdc extension, replace it with .mdc.example
    if (filename.endsWith('.mdc')) {
      return filename.replace(/\.mdc$/, '.mdc.example');
    }
    // Otherwise, just append .example
    return filename + '.example';
  }
  return filename;
}

/**
 * Determines the type of document based on its filename
 */
function getDocumentType(filename) {
  const typeMap = {
    'architecture': ['technical_architecture', 'architecture', 'system_architecture'],
    'component': ['component', 'module'],
    'api': ['api', 'service', 'endpoint'],
    'feature': ['feature', 'story', 'user_story'],
    'database': ['database', 'data_model', 'schema'],
    'testing': ['test', 'quality', 'qa'],
    'standards': ['standards', 'coding_standards', 'style_guide'],
    'security': ['security', 'auth'],
    'configuration': ['config', 'settings', 'setup'],
    'frontend': ['frontend', 'ui', 'ux'],
    'task': ['task', 'sprint'],
    'bug': ['bug', 'issue', 'fix']
  };
  
  const lowerFilename = filename.toLowerCase();
  
  for (const [type, keywords] of Object.entries(typeMap)) {
    if (keywords.some(keyword => lowerFilename.includes(keyword))) {
      return type;
    }
  }
  
  // Process numbered prefixes
  if (/^\d+/.test(filename)) {
    if (lowerFilename.includes('market') || lowerFilename.includes('research')) return 'research';
    if (lowerFilename.includes('problem')) return 'problem';
    if (lowerFilename.includes('technical')) return 'architecture';
    if (lowerFilename.includes('component')) return 'component';
    if (lowerFilename.includes('database')) return 'database';
    if (lowerFilename.includes('frontend')) return 'frontend';
    if (lowerFilename.includes('roadmap')) return 'planning';
  }
  
  return 'general';
}

/**
 * Gets a description for a document based on its filename
 */
function getDocumentDescription(filename) {
  const descriptions = {
    '00_index.md': 'Visión general del proyecto',
    'feature_documentation.md': 'Especificaciones de funcionalidades',
    'bug_documentation.md': 'Gestión de bugs y control de calidad',
    'quick_task_documentation.md': 'Tareas y configuración',
    'technical_architecture.md': 'Arquitectura técnica detallada',
    'component_specification.md': 'Especificaciones de componentes',
    'api_specification.md': 'Documentación de APIs',
    'database_design.md': 'Diseño de base de datos',
    'architecture_decision_record.md': 'Registro de decisiones arquitectónicas',
    'quality_assurance.md': 'Aseguramiento de calidad',
    'coding_standards.md': 'Estándares de código',
    'security_framework.md': 'Marco de seguridad'
  };
  
  // Check for exact matches
  if (descriptions[filename]) {
    return descriptions[filename];
  }
  
  // Check for partial matches
  const lowerFilename = filename.toLowerCase();
  
  if (lowerFilename.includes('market') || lowerFilename.includes('research')) 
    return 'Investigación de mercado';
  if (lowerFilename.includes('architecture') || lowerFilename.includes('technical')) 
    return 'Arquitectura del sistema';
  if (lowerFilename.includes('component')) 
    return 'Especificación de componentes';
  if (lowerFilename.includes('api')) 
    return 'Documentación de API';
  if (lowerFilename.includes('database') || lowerFilename.includes('data')) 
    return 'Diseño de datos';
  if (lowerFilename.includes('feature')) 
    return 'Especificaciones de funcionalidades';
  if (lowerFilename.includes('user')) 
    return 'Investigación de usuarios';
  if (lowerFilename.includes('journey') || lowerFilename.includes('map')) 
    return 'Mapas de experiencia de usuario';
  if (lowerFilename.includes('empathy')) 
    return 'Mapas de empatía';
  if (lowerFilename.includes('story')) 
    return 'Historias de usuario';
  if (lowerFilename.includes('frontend')) 
    return 'Arquitectura frontend';
  if (lowerFilename.includes('test')) 
    return 'Estrategias de pruebas';
  if (lowerFilename.includes('rule')) 
    return 'Reglas y guías del proyecto';
  if (lowerFilename.includes('security')) 
    return 'Consideraciones de seguridad';
  if (lowerFilename.includes('task')) 
    return 'Gestión de tareas';
  if (lowerFilename.includes('meeting')) 
    return 'Notas de reuniones';
  if (lowerFilename.includes('progress')) 
    return 'Seguimiento de progreso';
  if (lowerFilename.includes('bug')) 
    return 'Documentación de bugs';
  
  // Default description
  return 'Documentación del proyecto';
}

module.exports = {
  generateMDC
}; 