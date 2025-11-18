from django.shortcuts import render
from .dnac_manager import DNAC_Manager
from .mongo_logger import MongoLogger

def home(request):
    """Home page with menu"""
    return render(request, 'home.html')

def authenticate(request):
    """Authenticate and show token"""
    dnac = DNAC_Manager()
    logger = MongoLogger()
    
    result = dnac.get_auth_token()
    
    # Log to MongoDB
    logger.log_request(
        action='authenticate',
        success=result['success'],
        error=result.get('error')
    )
    
    context = {
        'result': result,
        'token': result.get('token', 'Authentication Failed')
    }
    return render(request, 'authenticate.html', context)

def list_devices(request):
    """List all network devices"""
    dnac = DNAC_Manager()
    logger = MongoLogger()
    
    result = dnac.get_network_devices()
    
    # Log to MongoDB
    logger.log_request(
        action='list_devices',
        success=result['success'],
        error=result.get('error')
    )
    
    context = {
        'result': result,
        'devices': result.get('devices', [])
    }
    return render(request, 'devices.html', context)

def device_interfaces(request):
    """Show interfaces for a specific device"""
    dnac = DNAC_Manager()
    logger = MongoLogger()
    
    device_ip = request.GET.get('ip', '')
    result = None
    
    if device_ip:
        result = dnac.get_device_interfaces(device_ip)
        
        # Log to MongoDB
        logger.log_request(
            action='get_interfaces',
            device_ip=device_ip,
            success=result['success'],
            error=result.get('error')
        )
    
    context = {
        'device_ip': device_ip,
        'result': result,
        'interfaces': result.get('interfaces', []) if result else []
    }
    return render(request, 'interfaces.html', context)