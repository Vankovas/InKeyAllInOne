export function timeoutWaitForVariable(variable, onLoad, count, endTimeoutCount, timeoutDelay) {
	if (count === endTimeoutCount) throw 'Could not load user data on time';
	if (variable === null || variable === undefined)
		return setTimeout(function() {
			timeoutWaitForVariable(variable, onLoad, count + 1, endTimeoutCount, timeoutDelay);
		}, timeoutDelay);

	onLoad();
}
