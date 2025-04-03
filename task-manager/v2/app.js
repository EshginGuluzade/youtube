const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = process.env.PORT || 3000;

// App version and theme color (for demonstrating rolling updates)
const APP_VERSION = '2.0.0';
const THEME_COLOR = '#32a455'; // Green theme

// Configure PostgreSQL connection
const pool = new Pool({
  user: process.env.POSTGRES_USER || 'postgres',
  host: process.env.POSTGRES_HOST || 'db',
  database: process.env.POSTGRES_DB || 'taskdb',
  password: process.env.POSTGRES_PASSWORD || 'postgres',
  port: 5432,
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Create tasks table if not exists
const initDb = async () => {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('Database initialized successfully');
  } catch (err) {
    console.error('Error initializing database:', err);
    // Retry after a delay
    setTimeout(initDb, 5000);
  }
};

// Initialize database
initDb();

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', version: APP_VERSION });
});

// HTML front-end
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Task Manager</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 20px;
          background-color: ${THEME_COLOR};
          color: white;
        }
        .container {
          max-width: 800px;
          margin: 0 auto;
          background-color: rgba(255, 255, 255, 0.1);
          padding: 20px;
          border-radius: 5px;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h1 {
          text-align: center;
        }
        .form-group {
          margin-bottom: 15px;
        }
        label {
          display: block;
          margin-bottom: 5px;
        }
        input, textarea, select {
          width: 100%;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }
        button {
          background-color: #2c3e50;
          color: white;
          border: none;
          padding: 10px 15px;
          border-radius: 4px;
          cursor: pointer;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
        }
        th, td {
          border: 1px solid rgba(255, 255, 255, 0.2);
          padding: 10px;
          text-align: left;
        }
        th {
          background-color: rgba(0, 0, 0, 0.1);
        }
        .footer {
          text-align: center;
          margin-top: 20px;
          font-size: 12px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Task Manager</h1>
        <p>A simple task management application</p>
        
        <div class="form-group">
          <h2>Add New Task</h2>
          <form id="taskForm">
            <div class="form-group">
              <label for="title">Title:</label>
              <input type="text" id="title" name="title" required>
            </div>
            <div class="form-group">
              <label for="description">Description:</label>
              <textarea id="description" name="description"></textarea>
            </div>
            <button type="submit">Add Task</button>
          </form>
        </div>
        
        <div>
          <h2>Task List</h2>
          <table id="taskTable">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Status</th>
                <th>Created At</th>
              </tr>
            </thead>
            <tbody id="taskList">
              <!-- Tasks will be loaded here -->
            </tbody>
          </table>
        </div>
        
        <div class="footer">
          <p>Task Manager v${APP_VERSION} | Running on Node.js with PostgreSQL</p>
        </div>
      </div>

      <script>
        // Load tasks when page loads
        document.addEventListener('DOMContentLoaded', fetchTasks);
        
        // Handle form submission
        document.getElementById('taskForm').addEventListener('submit', async (e) => {
          e.preventDefault();
          const title = document.getElementById('title').value;
          const description = document.getElementById('description').value;
          
          try {
            const response = await fetch('/api/tasks', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ title, description }),
            });
            
            if (response.ok) {
              document.getElementById('title').value = '';
              document.getElementById('description').value = '';
              fetchTasks();
            }
          } catch (error) {
            console.error('Error adding task:', error);
          }
        });
        
        // Fetch all tasks
        async function fetchTasks() {
          try {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            const taskList = document.getElementById('taskList');
            
            taskList.innerHTML = '';
            tasks.forEach(task => {
              const row = document.createElement('tr');
              row.innerHTML = \`
                <td>\${task.id}</td>
                <td>\${task.title}</td>
                <td>\${task.description || ''}</td>
                <td>\${task.status}</td>
                <td>\${new Date(task.created_at).toLocaleString()}</td>
              \`;
              taskList.appendChild(row);
            });
          } catch (error) {
            console.error('Error fetching tasks:', error);
          }
        }
      </script>
    </body>
    </html>
  `);
});

// API endpoints
app.get('/api/tasks', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM tasks ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    console.error('Error fetching tasks:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/tasks', async (req, res) => {
  const { title, description } = req.body;
  
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  
  try {
    const result = await pool.query(
      'INSERT INTO tasks (title, description) VALUES ($1, $2) RETURNING *',
      [title, description]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error creating task:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Task Manager app listening at http://localhost:${port}`);
  console.log(`Version: ${APP_VERSION}`);
});