const { spawn } = require('child_process');

const args = [
    'http',
    '127.0.0.1:11434',
    '--host-header', 'rewrite',
    '--response-header-add', 'X-Email: 24ds3000006@ds.study.iitm.ac.in',
    '--response-header-add', 'Access-Control-Expose-Headers: *',
    '--response-header-add', 'Access-Control-Allow-Headers: Authorization,Content-Type,User-Agent,Accept,Ngrok-skip-browser-warning'
];

const ngrok = spawn('ngrok', args, { stdio: 'inherit' });

ngrok.on('error', (err) => {
    console.error('Failed to start ngrok:', err);
});
