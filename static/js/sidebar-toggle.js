// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sidebar toggle script loaded');
    
    // Wait a bit for all elements to be rendered
    setTimeout(function() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const toggleIcon = document.getElementById('toggleIcon');
        
        console.log('Elements found:', {
            sidebar: !!sidebar,
            sidebarToggle: !!sidebarToggle,
            toggleIcon: !!toggleIcon
        });
        
        if (!sidebar || !sidebarToggle) {
            console.error('Required elements not found');
            return;
        }
        
        // Load saved state
        const savedState = localStorage.getItem('sidebarCollapsed');
        if (savedState === 'true') {
            sidebar.classList.add('collapsed');
        }
        
        // Simple click handler
        sidebarToggle.onclick = function(e) {
            console.log('Button clicked!');
            e.preventDefault();
            e.stopPropagation();
            
            // Toggle class
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                localStorage.setItem('sidebarCollapsed', 'false');
                console.log('Sidebar expanded');
            } else {
                sidebar.classList.add('collapsed');
                localStorage.setItem('sidebarCollapsed', 'true');
                console.log('Sidebar collapsed');
            }
            
            return false;
        };
        
        // Also try addEventListener as backup
        sidebarToggle.addEventListener('click', function(e) {
            console.log('Event listener triggered');
            sidebarToggle.onclick(e);
        }, true);
        
    }, 100);
});