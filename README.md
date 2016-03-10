<h1>EmptyDB</h1>
<h2>Description</h2>
<p>A simple helper for create an empty database and user with admin privileges, pretended to be used as complement tool
in frameworks like Wordpress and Prestashop where we need to create this kind of database</p>
<h2>Usage</h2>
<p>The primary use is intended to be in command line terminal. If given no server password param will ask for it in
interactive shell.</p>
<h3>Params</h3>
<ul>
<li>-h Show help and params description</li>
<li>-u or --db_user for set the new database user name, if not entered a random string will generate as default</li>
<li>-p or --db_pass for set the new user password, if not entered a random string will generate as default</li>
<li>-U or --root_user for Database server root user, if not entered 'root' is used as default</li>
<li>-P or --root_pass for Database root password, if not entered will be asked in interactive shell</li>
<li>-d or --driver for Server host, mysql as default, more driver will be added soon</li>
<li>-l or --length Database user password length, 8 char as default value generated for user name and password both</li>
<li>-D or --db_name for Database name, if not set, a random string will be generated as default value</li>
</ul>