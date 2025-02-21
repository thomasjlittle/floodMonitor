from datapoint import ProcessedDataPoint
import logging

def make_report(
        flood_points: list[ProcessedDataPoint], 
        stage_threshold: float, 
        url: str,
        logger: logging.Logger = None
        ) -> str:
    
    if logger is None:
        logger = logging.getLogger(__name__)
        
    try:
        report_lines = [
            f"<p>The following are the points greater than the threshold of {stage_threshold}:</p>",
            "<ul>"
        ]
        
        for point in flood_points:
            report_lines.append(f"<li>{point}</li>")
        
        report_lines.append("</ul>")
        report_lines.append(f'<p>See the full report <a href="{url}">here</a>.</p>')
        
        logger.info("Successfully created report. Tgod.")
        return "\n".join(report_lines)
    
    except Exception:
        logger.error("Failed to make report. I am so ashamed.")
        return ""
