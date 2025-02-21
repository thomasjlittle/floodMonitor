from datapoint import ProcessedDataPoint
import logging

def make_report(
        points_over_low_threshold: list[ProcessedDataPoint], 
        points_above_high_threshold: list[ProcessedDataPoint], 
        low_stage_threshold: float, 
        high_stage_threshold: float, 
        url: str,
        logger: logging.Logger = None
        ) -> str:
    
    if logger is None:
        logger = logging.getLogger(__name__)
        
    try:
        # If there are no points over the threshold, return a message saying so
        if not points_over_low_threshold and not points_above_high_threshold:
            report_lines = [
                "<p>There are no points greater than the threshold.</p>",
                f'<p>See the full report <a href="{url}">here</a>.</p>'
            ]
            logger.info("No points greater than the threshold. Good job!")
            return "\n".join(report_lines)

        # Otherwise, create a report with the points over the threshold    
        report_lines = [
            f"<p>The following are the points greater than the threshold of {low_stage_threshold}:</p>",
            "<ul>"
        ]
        
        for point in points_over_low_threshold:
            report_lines.append(f"<li>{point}</li>")

        # If there are points over 7.5, add them to the report
        if points_above_high_threshold:
            report_lines.append("</ul>")
            report_lines.append(f"<p>The following are the points greater than the threshold of {high_stage_threshold}:</p>")
            report_lines.append("<ul>")
            for point in points_above_high_threshold:
                report_lines.append(f"<li>{point}</li>")
        
        report_lines.append("</ul>")
        report_lines.append(f'<p>See the full report <a href="{url}">here</a>.</p>')
        
        logger.info("Successfully created report. Tgod.")
        return "\n".join(report_lines)
    
    except Exception:
        logger.error("Failed to make report. I am so ashamed.")
        return ""
