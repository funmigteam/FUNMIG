


self.addEventListener('install', (event) => {
    console.log('Service Worker installed');
    self.skipWaiting();
});


self.addEventListener('activate', (event) => {
    console.log('Service Worker activated');
    event.waitUntil(clients.claim());
});


self.addEventListener('push', (event) => {
    console.log('Push notification received');
    
    let data = {};
    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data = { title: 'فان میگ', body: event.data.text() };
        }
    }

    const title = data.title || 'فان میگ';
    const options = {
        body: data.body || 'پیام جدید دارید',
        icon: '/static/logo.png',
        badge: '/static/logo.png',
        vibrate: [100, 50, 100],
        data: {
            url: data.url || '/'
        },
        actions: [
            { action: 'open', title: 'باز کردن' },
            { action: 'close', title: 'بستن' }
        ],
        tag: data.tag || 'funmig-notification',
        renotify: true
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});


self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'close') {
        return;
    }

    const urlToOpen = event.notification.data?.url || '/';
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                
                for (const client of clientList) {
                    if (client.url === urlToOpen && 'focus' in client) {
                        return client.focus();
                    }
                }
                
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
    );
});


self.addEventListener('message', (event) => {
    console.log('SW received message:', event.data);
    
    if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
        const { title, body, url, tag } = event.data;
        
        self.registration.showNotification(title, {
            body: body,
            icon: '/static/logo.png',
            badge: '/static/logo.png',
            vibrate: [100, 50, 100],
            data: { url: url || '/' },
            tag: tag || 'funmig-message',
            renotify: true
        });
    }
});