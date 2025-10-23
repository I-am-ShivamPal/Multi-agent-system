import json
import datetime
import os

def send_message_to_mcp(agent_name, status, message_data):
    """
    Placeholder stub for Message Compute Plane (MCP) integration.
    
    In a real system, this function would serialize the message and send it
    to a message queue (like RabbitMQ, Kafka) or a gRPC endpoint for Ritesh's team.
    
    This stub simply formats the message as JSON, logs it to a file, 
    and prints it to the console.
    
    Args:
        agent_name (str): The name of the agent sending the message (e.g., "IssueDetector").
        status (str): A high-level status (e.g., "Detected", "Resolved").
        message_data (dict): A dictionary of the specific event details.
    """
    
    message = {
        "agent": agent_name,
        "status": status,
        "data": message_data,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Convert the dictionary to a JSON string with indentation for readability
    json_message = json.dumps(message, indent=2)
    
    print("\n" + "="*40)
    print(f"MCP STUB: Simulated Message from {agent_name}")
    print(json_message)
    print("="*40)
    
    # In a real system, this is where the message would be sent:
    # e.g., mcp_client.send(json_message)
    
    # For demonstration, we can also log this to a separate MCP log
    log_path = os.path.join("logs", "mcp_messages.log")
    os.makedirs("logs", exist_ok=True)
    with open(log_path, 'a') as f:
        f.write(json_message + "\n" + "-"*40 + "\n")

# This part allows you to run `python mcp_stub.py` directly to see an example
if __name__ == "__main__":
    print("Running `mcp_stub.py` directly to show an example message:")
    
    example_data = {
        "failure_state": "latency_issue",
        "reason": "High latency detected: 21000.50 ms",
        "dataset": "dataset/student_scores.csv"
    }
    
    send_message_to_mcp(
        agent_name="IssueDetector",
        status="Detected",
        message_data=example_data
    )
    
    example_data_2 = {
        "action_taken": "retry_deployment",
        "result": "success",
        "response_time_ms": 200
    }
    
    send_message_to_mcp(
        agent_name="RLOptimizer",
        status="Resolved",
        message_data=example_data_2
    )

