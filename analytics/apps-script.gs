/**
 * TakeHome — input analytics collector.
 * Receives POSTs from the website and appends one row per event to a Google Sheet.
 *
 * Setup: see analytics/README.md
 */
const SHEET_NAME = 'inputs';

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.tryLock(5000);
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['received_at', 'session', 'event', 'client_time', 'tax_year', 'state', 'tab', 'detail', 'inputs_json']);
    }
    const d = JSON.parse(e.postData.contents);
    sheet.appendRow([
      new Date(),
      String(d.sid || '').slice(0, 40),
      String(d.event || '').slice(0, 20),
      String(d.at || '').slice(0, 30),
      Number(d.year) || '',
      String(d.state || '').slice(0, 4),
      String(d.tab || '').slice(0, 10),
      String(d.detail || '').slice(0, 60),
      d.inputs ? JSON.stringify(d.inputs).slice(0, 4000) : '',
    ]);
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('err');
  } finally {
    lock.releaseLock();
  }
}
