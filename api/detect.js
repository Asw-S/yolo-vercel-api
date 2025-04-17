const { spawn } = require('child_process');

export default function handler(req, res) {
  if (req.method === 'POST') {
    let body = '';

    req.on('data', chunk => {
      body += chunk;
    });

    req.on('end', () => {
      try {
        const inputData = JSON.parse(body);

        const python = spawn('python3', ['api/detect.py', JSON.stringify(inputData)]);

        let result = '';
        python.stdout.on('data', data => {
          result += data.toString();
        });

        python.stderr.on('data', data => {
          console.error(`stderr: ${data}`);
        });

        python.on('close', code => {
          if (code === 0) {
            try {
              const jsonResponse = JSON.parse(result);
              res.status(200).json(jsonResponse);
            } catch (err) {
              res.status(500).json({ error: 'Failed to parse Python output', details: result });
            }
          } else {
            res.status(500).json({ error: 'Python script exited with code ' + code });
          }
        });
      } catch (err) {
        res.status(400).json({ error: 'Invalid JSON input' });
      }
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
