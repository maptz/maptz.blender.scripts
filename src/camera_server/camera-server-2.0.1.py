from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import bpy
from random import randint
import queue
import json
from functools import partial
from urllib.parse import urlparse
print("Running camera-server-2.0.1")

execution_queue = queue.Queue()
END_REQUESTED = False

def get_camera_attributes():
    obj_camera = bpy.context.scene.camera
    retval = {}
    # print ("JSON: Camera: " + str(obj_camera.name))
    if (bpy.context.scene.VisibilityProps is not None):
        retval["visibility_set"] = bpy.context.scene.VisibilityProps.sets
    retval["name"] = obj_camera.name
    retval["rotation_euler_x"] = obj_camera.rotation_euler.x
    retval["rotation_euler_y"] = obj_camera.rotation_euler.y
    retval["rotation_euler_z"] = obj_camera.rotation_euler.z
    retval["location_x"] = obj_camera.location.x
    retval["location_y"] = obj_camera.location.y
    retval["location_z"] = obj_camera.location.z
    retval["lens"] = obj_camera.data.lens
    retval["type"] = obj_camera.data.type
    retval["ortho_scale"] = obj_camera.data.ortho_scale
    retval_str = json.dumps(retval)
    return retval_str

def set_camera_attributes(camera_attributes):
    obj_camera = bpy.context.scene.camera
    obj_camera.rotation_euler.x = camera_attributes["rotation_euler_x"]
    obj_camera.rotation_euler.y = camera_attributes["rotation_euler_y"]
    obj_camera.rotation_euler.z = camera_attributes["rotation_euler_z"]
    obj_camera.location.x = camera_attributes["location_x"]
    obj_camera.location.y = camera_attributes["location_y"]
    obj_camera.location.z = camera_attributes["location_z"]
    obj_camera.data.lens = camera_attributes["lens"]
    obj_camera.data.type = camera_attributes["type"]
    obj_camera.data.ortho_scale = camera_attributes["ortho_scale"]

    if ((bpy.context.scene.set_visibility is not None) and ("visibility_set" in camera_attributes)):
        bpy.context.scene.set_visibility(camera_attributes["visibility_set"])
    #bpy.context.scene.update()

def set_camera_fn(camera_attributes_json):
    def sc(ctx):
        camera_attributes = json.loads(camera_attributes_json)
        set_camera_attributes(camera_attributes)
    return sc


def run_in_main_thread(function):
    print(threading.current_thread().name, "Adding function string to queue")
    execution_queue.put(function)

def end(ctx):
    global END_REQUESTED
    print("Exit requested")
    END_REQUESTED = True
    httpServer.stop()

def addSimpleCube(ctx):
    print(threading.current_thread().name, "Executing addSimpleCube function")
    bpy.ops.mesh.primitive_cube_add(location=(randint(-10,10),randint(-10,10),randint(-10,10)))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(threading.current_thread().name, "handle get")
        parsed_path = urlparse(self.path)
        print("GET: " + parsed_path.path)
        if (parsed_path.path == "/new"):
            run_in_main_thread(addSimpleCube)
            print("'new' queued.")
        elif  (parsed_path.path == "/ping"):
            pass
        elif (parsed_path.path == "/get"):
            strss = get_camera_attributes()
            print("'get': " + strss)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")      
            self.end_headers()
            self.wfile.write(strss.encode())
            return
        elif (parsed_path.path == "/viewport"):
            vp_file="e:\\test.jpg"
            bpy.context.scene.render.image_settings.file_format='JPEG'
            bpy.context.scene.render.filepath = vp_file
            bpy.ops.render.render(use_viewport = True, write_still=True)
            f = open(vp_file, 'rb')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-type', 'image/jpeg')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")      
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

        elif (parsed_path.path == "/exit"):
            print("'exit' queued")
            run_in_main_thread(end)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.end_headers()
        self.wfile.write(b'Success!\n')
    def log_message(self, format, *args):
        return
    def do_POST(self):
        parsed_path = urlparse(self.path)
        print("SET: " + parsed_path.path)
        if (parsed_path.path == "/set"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            bodyStr = body.decode('utf-8')
            run_in_main_thread(set_camera_fn(bodyStr))
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
            self.end_headers()
            self.wfile.write(b'Success!\n')
            return
        self.send_response(404)

 
class ServerThread(threading.Thread):
     stopped = False
     should_be_running = 0
     httpd = None
     def __init__(self,port):
         super(ServerThread, self).__init__()
         self.port=port
 
     def run(self):
         print("SERVER running on port " + str(self.port))
         self.should_be_running = 1
         self.httpd = HTTPServer(('localhost', self.port), SimpleHTTPRequestHandler)
         self.httpd.serve_forever()
            
     
     def stop(self):
         self.should_be_running = 0
         self.httpd.shutdown()
         print("SERVER down")
        #  self.httpd.server_close()
 
httpServer = ServerThread(8000)
httpServer.setDaemon(True)
httpServer.start()


def execute_queued_functions():
    window = bpy.context.window_manager.windows[0]
    ctx = {'window': window, 'screen': window.screen}  
    #print(threading.current_thread().name, "timer consuming queue")
    while not execution_queue.empty():
        function = execution_queue.get()        
        print(threading.current_thread().name, "function found name:", function)
        function(ctx)
    
    if (END_REQUESTED):
            print("Ending timer thread")
            bpy.app.timers.unregister(execute_queued_functions)
            bpy.ops.wm.quit_blender()
    return 1.0

bpy.app.timers.register(execute_queued_functions)