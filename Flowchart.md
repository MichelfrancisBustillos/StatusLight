# StatusLight Program Flowchart

## Application Flow

```mermaid
graph TD
    A[Start Application] --> B{Config File Exists?}
    B -->|No| C[Generate Default Config]
    C --> D[Load Config]
    B -->|Yes| D
    D --> E{Command Line Args?}
    E -->|Light IP Provided| F[Update Light IP from Args]
    F --> G[Load Config]
    E -->|No Args| G
    G --> H[Create GUI Window]
    H --> I[Display GUI with 3 Tabs]
    I --> J{User Action}
```

## Main Status Update Loop

```mermaid
graph TD
    A[Update Status Called] --> B[Check Light Communication]
    B --> C{Light Connected?}
    C -->|No| D[Show Error Message]
    D --> E[Update Light Status Label: Error]
    C -->|Yes| F{Manual Override Enabled?}
    F -->|Yes| G[Use Manually Set Status]
    F -->|No| H[Extract Status from Teams Log]
    H --> I{Status Changed?}
    I -->|Yes| J[Update Light with New Color]
    I -->|No| K[Keep Current Light State]
    G --> L{Status Different from Light?}
    L -->|Yes| J
    L -->|No| K
    J --> M[Update Status Label]
    M --> N[Schedule Next Update in 10s]
    K --> N
    E --> O[End Update]
    N --> O
```

## GUI Tabs and User Interactions

```mermaid
graph TD
    A[GUI Main Window] --> B[Tab Selection]
    B --> C{Which Tab?}
    
    C -->|Status Tab| D["Display Current Status<br/>Display Light Status"]
    
    C -->|Control Tab| E["Manual Override Checkbox"]
    E --> F{Override Enabled?}
    F -->|Yes| G["Enable Status Buttons<br/>Set Busy/Away/Available/Off"]
    F -->|No| H["Disable Status Buttons<br/>Auto-update from Teams"]
    G --> I["User Clicks Button"]
    I --> J["Call update_status with<br/>Selected Status"]
    
    C -->|Settings Tab| K["Configure Light IP"]
    K --> L["Save Light IP"]
    L --> M["Validate Connection"]
    
    K --> N["Choose Color for Status<br/>Busy/Away/Available"]
    N --> O["Save Color to Config"]
    
    K --> P["Enable Minimize to Tray"]
    
    K --> Q["Set Teams Log Path"]
    Q --> R["Save Log Path to Config"]
    
    K --> S["Reset to Default Config"]
```

## Teams Status Extraction

```mermaid
graph TD
    A[Extract Status Called] --> B[Get Teams Log Path from Config]
    B --> C{Log File Found?}
    C -->|No| D[Show Error Message]
    D --> E[Return Error Status]
    C -->|Yes| F[Open Log File with mmap]
    F --> G[Search for Latest Status Entry]
    G --> H{Status Found?}
    H -->|No| I[Return Unknown]
    H -->|Yes| J[Parse Status Value]
    J --> K{Match Known Status?}
    K -->|Available| L[Return Available]
    K -->|Busy| M[Return Busy]
    K -->|Away| N[Return Away]
    K -->|Do Not Disturb| O[Return Busy]
    K -->|No Match| P[Return Unknown]
```

## Light Communication and Update

```mermaid
graph TD
    A[Update Light Called] --> B[Get Light IP URL from Config]
    B --> C[Get RGB Values for Status<br/>from Config]
    C --> D[Build Color Payload]
    D --> E[POST Request to Light]
    E --> F{Request Successful?}
    F -->|Yes| G[Log Success]
    F -->|No| H[Log Error]
    
    I[Light Communications Check] --> J[GET Request to Light URL]
    J --> K{Response OK?}
    K -->|Yes| L[Return Connected]
    K -->|No| M[Set Error Status Flag]
    M --> N[Show Error Dialog]
    N --> O[Return Error]
```

## Configuration Management

```mermaid
graph TD
    A[Load Config] --> B[Read config.ini]
    B --> C[Parse Settings Section]
    C --> D[Load into Global Dict:<br/>light_ip, light_url<br/>busy_color, away_color<br/>available_color<br/>teams_log_path<br/>tray_minimize<br/>manual_override]
    
    E[Save Config] --> F{What to Update?}
    F -->|Light IP| G[Update light_ip]
    F -->|Status Color| H[Update busy/away/available color]
    F -->|Tray Minimize| I[Update tray_minimize]
    F -->|Manual Override| J[Update manual_override]
    F -->|Teams Log Path| K[Update teams_log_path]
    G --> L[Write to config.ini]
    H --> L
    I --> L
    J --> L
    K --> L
    L --> M[Reload Config]
```

## System Tray Integration

```mermaid
graph TD
    A[Window Close Button] --> B{Tray Minimize Enabled?}
    B -->|Yes| C[Withdraw Window to Tray]
    C --> D[Get Current Status]
    D --> E[Load Icon Image]
    E --> F[Show Tray Icon]
    F --> G{Tray Menu Selection}
    G -->|Open| H[Show Window]
    G -->|Exit| I[Stop Icon]
    I --> J[Destroy Application]
    H --> K[Stop Icon]
    K --> L[Restore Window]
    B -->|No| M[Close Application Directly]
```
