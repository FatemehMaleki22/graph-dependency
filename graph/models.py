from django.db import models

# Create your models here.
class Node(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Edge(models.Model):
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')

    def __str__(self):
        return f"{self.source} → {self.target}"
