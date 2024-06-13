def replace_asterisks(input_string):
    result = []
    asterisk_count = 0
    ignore = False

    i = 0
    while i < len(input_string):
        if input_string[i] == '*':
            if ignore:
                result.append('*')
                i += 1
                continue
            
            if asterisk_count % 2 == 0:
                start = i
                end = input_string.find('*', start + 1)
                if end == -1:
                    result.append(input_string[i:])
                    break
                if ' ' in input_string[start:end]:
                    ignore = True
                    result.append('*')
                else:
                    result.append('<strong>')
                    asterisk_count += 1
            else:
                result.append('</strong>')
                asterisk_count += 1
        else:
            result.append(input_string[i])
        i += 1

        if asterisk_count % 2 == 0:
            ignore = False

    return ''.join(result)


def replace_custom_tags(symbol,replacement,input_string):
    result = []
    i = 0
    while i < len(input_string):
        if input_string[i:i+2] == symbol[0]:
            start = i
            end = input_string.find(symbol[1], start + 2)
            if end == -1:
                result.append(input_string[i:])
                break
            
            result.append(replacement[0])
            result.append(input_string[start + 2:end])
            result.append(replacement[1])
            i = end + 2
        else:
            result.append(input_string[i])
            i += 1

    return ''.join(result)

class EmailNoreplyTemplates:
    def __init__(self):
        pass
    def cleanProfessional(self,mail_data):
       
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                {f"<h1 style='color: #4CAF50;'>{mail_data.header},</h1>" if mail_data.header else "" }
                {mail_data.body if mail_data.body else ""}
                <br>
                {mail_data.footer if mail_data else ""}
            </body>
        </html>
        
        """
        body = replace_asterisks(body)
        body = replace_custom_tags(("[>","<]"),("<div style='border-left: 4px solid #4CAF50; padding-left: 10px; margin-top: 10px;'>","</div>"),body)
        body = body.replace("\n","<br>")
        return body 

class EmailContactTemplates:
    def __init__(self):
        pass
    def cleanProfessional(self,api_title, mail_data):
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h1 style="color: #4CAF50;">Hello,</h1>
                <p>This is a message from HloMail. You received a new interaction today on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                <p><strong>Message:</strong></p>
                <div style="border-left: 4px solid #4CAF50; padding-left: 10px; margin-top: 10px;">
                    <p>{mail_data.message}</p>
                </div>
                <br>
                <p>Best regards,<br>HloMail Team</p>
            </body>
        </html>

        """
        return body

    def modernMinimalist(self,api_title, mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.5; color: #333;">
                <h1 style="color: #2196F3; text-align: center;">Hello,</h1>
                <p style="text-align: center;">You have a new message on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px;">
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <p>{mail_data.message}</p>
                </div>
                <br>
                <p style="text-align: center;">Best regards,<br>HloMail Team</p>
            </body>
        </html>

        """
        return body

    def elegantStylish(self,api_title, mail_data):
        body = f"""
        <html>
            <body style="font-family: Georgia, serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
                <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h1 style="color: #e91e63;">Hello,</h1>
                    <p>You have a new interaction on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="border-left: 4px solid #e91e63; padding-left: 10px; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Best regards,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body

    def classicFormal(self,api_title, mail_data):
        body = f"""
        <html>
            <body style="font-family: Times New Roman, Times, serif; line-height: 1.6; color: #333;">
                <h1 style="color: #000080;">Greetings,</h1>
                <p>You have received a new message on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                <p><strong>Message:</strong></p>
                <blockquote style="margin: 10px 0; padding: 10px; background-color: #f0f0f0; border-left: 4px solid #000080;">
                    <p>{mail_data.message}</p>
                </blockquote>
                <br>
                <p>Yours sincerely,<br>HloMail Team</p>
            </body>
        </html>

        """
        return body

    def vibrantEnergetic(self,api_title, mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Trebuchet MS', Helvetica, sans-serif; line-height: 1.6; color: #333; background-color: #fffbcc; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; border: 2px solid #ff9800;">
                    <h1 style="color: #ff9800;">Hey there,</h1>
                    <p>Exciting news! You've got a new message on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="background-color: #fff3e0; padding: 10px; border-left: 4px solid #ff9800; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Cheers,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body
    def boldVibrant(self,api_title,mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Verdana', sans-serif; line-height: 1.6; color: #444; background-color: #f2f2f2; padding: 20px;">
                <div style="background-color: #fff; padding: 20px; border-radius: 10px; border-top: 5px solid #ff5722;">
                    <h1 style="color: #ff5722;">Hello!</h1>
                    <p>You have a new message on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="border-left: 4px solid #ff5722; padding-left: 10px; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Best regards,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body
    def softCalm(self,api_title,mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; line-height: 1.6; color: #555; background-color: #e0f7fa; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #b2ebf2;">
                    <h1 style="color: #00acc1;">Greetings!</h1>
                    <p>You have received a new message on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="border-left: 4px solid #00acc1; padding-left: 10px; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Kind regards,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body

    def luxuriousElegant(self,api_title,mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Georgia', serif; line-height: 1.6; color: #333; background-color: #f8f8f8; padding: 20px;">
                <div style="background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <h1 style="color: #b71c1c;">Dear User,</h1>
                    <p>You have a new interaction on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="border-left: 4px solid #b71c1c; padding-left: 10px; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Best wishes,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body

    def funFriendly(self,api_title,mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Comic Sans MS', 'Comic Sans', cursive; line-height: 1.6; color: #444; background-color: #fff8e1; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #ffeb3b;">
                    <h1 style="color: #ffeb3b;">Hey there!</h1>
                    <p>You have an exciting new message on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="border-left: 4px solid #ffeb3b; padding-left: 10px; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Take care,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body
    def sleekModern(self,api_title,mail_data):
        body = f"""
        <html>
            <body style="font-family: 'Roboto', sans-serif; line-height: 1.6; color: #333; background-color: #eeeeee; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border-top: 5px solid #607d8b;">
                    <h1 style="color: #607d8b;">Hello,</h1>
                    <p>This is a message from HloMail. You received a new interaction today on <strong>{api_title}</strong> from <strong>{mail_data.name if mail_data.name else "New Customer"}</strong>.</p>
                    {f"<p><strong>Name:</strong> {mail_data.name}</p>" if mail_data.name else ""}
                    {f"<p><strong>Email:</strong> {mail_data.email}</p>" if mail_data.email else ""}
                    {f"<p><strong>Phone Number:</strong> {mail_data.phone_no}</p>" if mail_data.phone_no else ""}
                    <p><strong>Message:</strong></p>
                    <div style="border-left: 4px solid #607d8b; padding-left: 10px; margin-top: 10px;">
                        <p>{mail_data.message}</p>
                    </div>
                    <br>
                    <p>Best regards,<br>HloMail Team</p>
                </div>
            </body>
        </html>

        """
        return body

