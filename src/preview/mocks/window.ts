export function getCurrentWindow() {
  return {
    setTitle: async () => {},
    show: async () => {},
    setFocus: async () => {},
    onCloseRequested: async () => () => {},
  };
}
