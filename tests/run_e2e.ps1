$env:COORD_EMAIL="dev@inforcoopecipa.it"
$env:COORD_PASSWORD="final"
$env:OP_EMAIL="colline@inforcoopecipa.it"
$env:OP_PASSWORD="colline!"
npx playwright test tests/e2e/prenotazioni.spec.js --reporter=line