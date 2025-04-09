from fastapi import APIRouter
from fastapi.responses import JSONResponse
from django.apps import apps

router = APIRouter()

def get_nodes_and_edges():
    Node = apps.get_model('graph', 'Node')
    Edge = apps.get_model('graph', 'Edge')

    nodes = Node.objects.all()
    edges = Edge.objects.all()

   
    nodes_data = [{"id": node.id, "label": node.label} for node in nodes]
    edges_data = [{"from": edge.source.id, "to": edge.target.id} for edge in edges]

    return nodes_data, edges_data

@router.get("/graph")
def get_graph():
    try:
        
        nodes_data, edges_data =  get_nodes_and_edges()

        return JSONResponse(content={"nodes": nodes_data, "edges": edges_data})

    except Exception as e:
        print(f"Error fetching graph data: {e}")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)