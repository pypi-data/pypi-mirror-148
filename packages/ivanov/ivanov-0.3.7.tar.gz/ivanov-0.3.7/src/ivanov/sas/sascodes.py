from string import Template

extract_lib_template = Template("""
%let metasrv="${metadata_server}";
%let metaprt=${metadata_port};
%let metausr="${metadata_user}";
%let metapwd="${metadata_password}";
%let metarep="${metadata_repo}";

%macro libsfromrepo(mdrep=);
/*************************************************************/

/*%macro getMetaInfos(EXCELFILE,OUTPUTFORMAT);*/
  data metadata_libraries;
  length uri serveruri conn_uri domainuri conns_uri serv_uri propuri libname ServerContext AuthDomain path_schema
         usingpkguri type tableuri coluri $256 id $17
         desc $200 libref engine $8 isDBMS $1 DomainLogin  $32
		 Server_connection $100 Server_meta $50 TnsODBC $50 TnsODBC2 $50
			repo $50;
  /*keep libname desc libref engine ServerContext path_schema AuthDomain table colname
      coltype collen IsPreassigned IsDBMSLibname id Server_connection Server_meta TnsODBC TnsODBC2;*/
  keep libname desc libref engine ServerContext path_schema AuthDomain  
        IsPreassigned /*IsDBMSLibname*/ /*id*/ Server_connection Server_meta TnsODBC TnsODBC2 repo;

  nobj=.;
  n=1;
  uri='';
  serveruri='';
  conn_uri='';
  domainuri='';

         /***Determine how many libraries there are***/
  nobj=metadata_getnobj("omsobj:SASLibrary?@Id contains '.'",n,uri);
         /***Retrieve the attributes for all libraries, if there are any***/
  if n>0 then do n=1 to nobj;
    libname='';
    ServerContext='';
    AuthDomain='';
    desc='';
    libref='';
    engine='';
    isDBMS='';
    IsPreassigned='';
    IsDBMSLibname='';
    path_schema='';
    usingpkguri='';
    type='';
    id='';
	Server_connection='';
	Server_meta='';
	TnsODBC='';
	TnsODBC2='';

    nobj=metadata_getnobj("omsobj:SASLibrary?@Id contains '.'",n,uri);
    rc= metadata_getattr(uri, "Name", libname);
    rc= metadata_getattr(uri, "Desc", desc);
    rc= metadata_getattr(uri, "Libref", libref);
    rc= metadata_getattr(uri, "Engine", engine);
    rc= metadata_getattr(uri, "IsDBMSLibname", isDBMS);
    rc= metadata_getattr(uri, "IsDBMSLibname", IsDBMSLibname); 
    rc= metadata_getattr(uri, "IsPreassigned", IsPreassigned); 
    rc= metadata_getattr(uri, "Id", Id);

    /*** Get associated ServerContext ***/
    i=1;
    rc= metadata_getnasn(uri, "DeployedComponents", i, serveruri);
    if rc > 0 then rc2= metadata_getattr(serveruri, "Name", ServerContext);
    else ServerContext='';

    /*** If the library is a DBMS library, get the Authentication Domain
         associated with the DBMS connection credentials ***/
    if isDBMS="1" then do;
      i=1; 
      rc= metadata_getnasn(uri, "LibraryConnection", i, conn_uri);
      if rc > 0 then do;
        rc2= metadata_getnasn(conn_uri, "Domain", i, domainuri);
        if rc2 > 0 then do;
			rc3= metadata_getattr(domainuri, "Name", AuthDomain);
			rc4=metadata_getnasn(domainuri, "Connections", i, conns_uri);
			if rc4>0 then do;
				rc4=metadata_getattr(conns_uri, "Name", Server_connection);
				rc5=metadata_getnasn(conns_uri, "Source", i, serv_uri);
				if rc5>0 then do;
					rc5=metadata_getattr(serv_uri, "Name", Server_meta);
				end;
			end;
		end;
		rc2=metadata_getnasn(conn_uri, "Properties", i, propuri);
		if rc2 > 0 then do;
			rc3=metadata_getattr(propuri, "DefaultValue", TnsODBC);
		end;

		rc2_2=metadata_getnasn(conn_uri, "Properties", 2, propuri);
		if rc2_2 > 0 then do;
			rc3=metadata_getattr(propuri, "DefaultValue", TnsODBC2);
		end;

      end;
    end;

    /*** Get the path/database schema for this library ***/
    rc=metadata_getnasn(uri, "UsingPackages", 1, usingpkguri);
    if rc>0 then do;
      rc=metadata_resolve(usingpkguri,type,id);  
      if type='Directory' then 
        rc=metadata_getattr(usingpkguri, "DirectoryName", path_schema);
      else if type='DatabaseSchema' then 
        rc=metadata_getattr(usingpkguri, "SchemaName", path_schema);
      else path_schema="unknown";
    end;
  repo="&mdrep";
  output;
    
  end;
 
 run;

 proc append base=Libraries_final
 	data=metadata_libraries;
%mend;


options /*metaserver="sasmeta.dwhgridprod.imb.ru"*/
		metaserver=&metasrv
        metaport=&metaprt
        metauser=&metausr
        metapass=&metapwd
        metarepository=&metarep;

/*получаем список репозиториев SAS*/


filename myoutput temp;

proc metadata 
out=myoutput
header=full
   in="<GetRepositories>
   <Repositories/> 
   <!-- OMI_ALL (1) flag -->
   <Flags>1</Flags>
    <Options/> 
   </GetRepositories>";
run;


filename getrepos temp;
libname getrepos xmlv2 xmlfileref=myoutput automap=replace xmlmap=getrepos;
proc copy in=getrepos out=work;
run;

proc sql;
	delete from Repository
	where Repository_name in ('REPOSMGR','BILineage');
quit;


data run;
	set Repository;
	str = catt('options metaserver=',&metasrv,' metaport=',&metaprt,' metauser="',&metausr,'" metapass="',&metapwd,'" metarepository="', Repository_Name,'";');
	str_macro = catt('%libsfromrepo(mdrep=', Repository_Name,');');
	call execute(str);
	call execute(str_macro);
run;

proc sql;
	delete from Libraries_final
	where libname ='';
quit;
""")